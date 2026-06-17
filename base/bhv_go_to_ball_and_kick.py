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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.player.player_agent import PlayerAgent


class BhvGoToBallAndKick:
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
