from lib.action.go_to_point import GoToPoint
from lib.action.intercept import Intercept
from lib.action.neck_scan_players import NeckScanPlayers
from lib.action.neck_turn_to_ball import NeckTurnToBall
from lib.action.neck_turn_to_ball_or_scan import NeckTurnToBallOrScan
from lib.action.scan_field import ScanField
from lib.action.smart_kick import SmartKick
from lib.debug.debug import log
from lib.rcsc.server_param import ServerParam
from lib.action.hold_ball import HoldBall
from base.generator_pass import BhvPassGen
from pyrusgeom.vector_2d import Vector2D
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.player.player_agent import PlayerAgent


class BhvGoToBallAndKick:
    DRIBBLE_DISTANCE = 4.0
    DRIBBLE_SPEED = 1.2
    SHOOT_AREA_MARGIN = 12.0

    def execute(self, agent: 'PlayerAgent'):
        wm = agent.world()
        sp = ServerParam.i()
        #terminal_debug = open('/dev/pts/4', 'w')

        if not wm.ball().pos_valid():
            log.debug_client().add_message('minimal_scan_ball')
            agent.set_neck_action(NeckTurnToBallOrScan())
            return ScanField().execute(agent)

        if wm.self().is_kickable():
            target = sp.their_team_goal_pos()
            first_speed = sp.ball_speed_max()

            dist_gol = wm.self().pos().dist(target)
            
            opp_min = wm.intercept_table().opponent_reach_cycle()
            if dist_gol < 20:
                SmartKick(target, 2, 2 * 0.6, 3).execute(agent)
                        
                #print(f"chutou distancia: {dist_gol:.2f}", file=terminal_debug)
                #print(f"alvo: x={target.x():.2f}, y={target.y():.2f}", file=terminal_debug)

                agent.set_neck_action(NeckScanPlayers())

                log.debug_client().set_target(target)
                log.debug_client().add_message('minimal_kick_to_goal')
            
                return 
            elif opp_min >= 5:
                SmartKick(target, 0.3, 0.1, 1).execute(agent)
                agent.set_neck_action(NeckScanPlayers())
                return 
            else:
                passe = BhvPassGen().generator(wm)
                if len(passe) > 0:
                    melhor_passe = max(passe)
                    #print(f"passou valor: {melhor_passe}", file=terminal_debug)
                    SmartKick(melhor_passe.target_ball_pos, melhor_passe.start_ball_speed, melhor_passe.start_ball_speed*0.6, 3).execute(agent)
                    agent.set_neck_action(NeckScanPlayers())
                    return True
            return True

        #log.debug_client().set_target(wm.ball().pos())
       # log.debug_client().add_message('minimal_go_to_ball')

        if Intercept().execute(agent):
            agent.set_neck_action(NeckTurnToBall())
            return True

        dist_thr = max(0.5, wm.self().player_type().kickable_area() * 0.5)
        if GoToPoint(wm.ball().pos(), dist_thr, sp.max_dash_power()).execute(agent):
            agent.set_neck_action(NeckTurnToBall())
            return True

        agent.set_neck_action(NeckTurnToBallOrScan())
        return True

    def _should_shoot(self, wm, sp):
        # Funcao auxiliar da nossa implementacao: identifica quando a bola ja
        # esta em regiao boa para finalizar. Nao substitui o fluxo principal.
        shoot_line_x = sp.their_penalty_area_line_x() - self.SHOOT_AREA_MARGIN
        goal_pos = sp.their_team_goal_pos()
        return wm.ball().pos().x() >= shoot_line_x or wm.self().pos().dist(goal_pos) < 20.0

    def _dribble_forward(self, agent: 'PlayerAgent', sp):
        wm = agent.world()
        ball_pos = wm.ball().pos()
        goal_pos = sp.their_team_goal_pos()

        # Drible simples: empurra a bola poucos metros em direcao ao gol.
        # A velocidade baixa permite que o jogador alcance a bola novamente.
        dribble_angle = (goal_pos - ball_pos).th()
        raw_target = ball_pos + Vector2D.polar2vector(self.DRIBBLE_DISTANCE, dribble_angle)
        target = self._keep_point_inside_pitch(raw_target, sp)

        log.debug_client().set_target(target)
        log.debug_client().add_message('dribble_forward')

        SmartKick(target, self.DRIBBLE_SPEED, self.DRIBBLE_SPEED * 0.7, 2).execute(agent)
        agent.set_neck_action(NeckTurnToBall())
        return True

    def _shoot_to_best_goal_target(self, agent: 'PlayerAgent', sp):
        wm = agent.world()
        target_name, target = self._select_best_goal_target(wm, sp)
        first_speed = sp.ball_speed_max()

        log.debug_client().set_target(target)
        log.debug_client().add_message(f'shoot_{target_name}')

        SmartKick(target, first_speed, first_speed * 0.8, 3).execute(agent)
        agent.set_neck_action(NeckScanPlayers())
        return True

    def _select_best_goal_target(self, wm, sp):
        # Testa tres alvos no gol: esquerdo, centro e direito.
        # A escolha favorece o ponto que fica mais longe do alcance do goleiro.
        goal_x = sp.pitch_half_length()
        corner_y = max(0.0, sp.goal_half_width() - 1.0)
        candidates = [
            ('canto_esquerdo', Vector2D(goal_x, corner_y)),
            ('centro', Vector2D(goal_x, 0.0)),
            ('canto_direito', Vector2D(goal_x, -corner_y)),
        ]

        goalie = wm.get_opponent_goalie()
        if goalie is None or goalie.unum() <= 0 or not goalie.pos().is_valid():
            return 'centro', candidates[1][1]

        best_name = 'centro'
        best_target = candidates[1][1]
        best_score = -float('inf')

        for name, target in candidates:
            score = self._goalie_reach_margin(wm, goalie, target, sp)
            if score > best_score:
                best_name = name
                best_target = target
                best_score = score

        return best_name, best_target

    def _goalie_reach_margin(self, wm, goalie, target, sp):
        # Margem positiva: a bola tende a chegar antes do goleiro.
        # Margem negativa: alvo arriscado, pois o goleiro pode chegar primeiro.
        ball_dist = wm.ball().pos().dist(target)
        ball_steps = sp.ball_move_step(sp.ball_speed_max(), ball_dist)
        if ball_steps < 0:
            ball_steps = 1000

        goalie_speed = max(0.1, goalie.player_type().real_speed_max())
        goalie_steps = goalie.pos().dist(target) / goalie_speed

        # Pequeno bonus para alvos mais afastados lateralmente do goleiro.
        lateral_gap = abs(target.y() - goalie.pos().y())
        return goalie_steps - ball_steps + lateral_gap * 0.1

    def _keep_point_inside_pitch(self, point, sp):
        # Evita conduzir a bola para fora do campo.
        x = max(-sp.pitch_half_length() + 1.0, min(sp.pitch_half_length() - 1.0, point.x()))
        y = max(-sp.pitch_half_width() + 1.0, min(sp.pitch_half_width() - 1.0, point.y()))
        return Vector2D(x, y)
