from base.decision import get_decision
from base.sample_communication import SampleCommunication
from base.view_tactical import ViewTactical
from base.bhv_go_to_ball_and_kick import BhvGoToBallAndKick
from base.generator_pass import BhvPassGen
from base.strategy_formation import StrategyFormation as Strategy
from lib.action.hold_ball import HoldBall
from lib.action.smart_kick import SmartKick
from lib.action.neck_scan_players import NeckScanPlayers
from lib.action.go_to_point import GoToPoint
from lib.action.intercept import Intercept
from lib.action.neck_body_to_ball import NeckBodyToBall
from lib.action.neck_turn_to_ball import NeckTurnToBall
from lib.action.neck_turn_to_ball_or_scan import NeckTurnToBallOrScan
from lib.action.scan_field import ScanField
from lib.debug.debug import log
from lib.debug.level import Level
from lib.player.player_agent import PlayerAgent
from lib.rcsc.server_param import ServerParam
from lib.rcsc.types import GameModeType
from pyrusgeom.vector_2d import Vector2D


class SamplePlayer(PlayerAgent):
    def __init__(self, goalie=False):
        super().__init__(goalie)
        self._communication = SampleCommunication()
        
    def action_impl(self):
        wm = self.world()
        numero = wm.self().unum()
        posicao = {
                1: (-48.0, 0.0),
                2: (-30.0, -15.0), 3: (-30.0, 0.0), 4: (-30.0, 15.0),
                5: (-15.0, -20.0), 6: (-15.0, -6.0), 7: (-15.0, 6.0), 8: (-15.0, 20.0),
                9: (-2.0, -15.0), 10: (-0.5, 0.0), 11: (-2.0, 15.0)
        }
        if self.do_preprocess():
            return
            
        if wm.game_mode().type() is not GameModeType.PlayOn:
            numero = wm.self().unum()
            
            if numero in posicao:
                x, y = posicao[numero]
                self.do_move(x, y) 
                
            self.set_neck_action(NeckTurnToBall())
            return

        if not wm.self().is_kickable():
            self_min = wm.intercept_table().self_reach_cycle()
            tm_min = wm.intercept_table().teammate_reach_cycle()
            
            if self_min <= tm_min:
                BhvGoToBallAndKick().execute(self)
            elif numero != 1:
                x_jogador, y_linha = posicao.get(numero, (0.0, 0.0))
                x_bola = wm.ball().pos().x()
                y_jogador = wm.self().pos().y()
                
                novo_x = x_bola + x_jogador
                destino = Vector2D(novo_x, y_jogador)
                
                GoToPoint(destino, 0.5, ServerParam.i().max_dash_power()).execute(self)
                self.set_neck_action(NeckTurnToBall())
        else:
            BhvGoToBallAndKick().execute(self)
            
    def do_preprocess(self):
        wm = self.world()

        if wm.self().is_frozen():
            self.set_view_action(ViewTactical())
            self.set_neck_action(NeckTurnToBallOrScan())
            return True

        if not wm.self().pos_valid():
            self.set_view_action(ViewTactical())
            ScanField().execute(self)
            return True

        count_thr = 10 if wm.self().goalie() else 5
        if wm.ball().pos_count() > count_thr or ( wm.game_mode().type() is not GameModeType.PlayOn and wm.ball().seen_pos_count() > count_thr + 10):
            self.set_view_action(ViewTactical())
            NeckBodyToBall().execute(self)
            return True

        self.set_view_action(ViewTactical())

        if self.do_heard_pass_receive():
            return True

        return False

    def do_heard_pass_receive(self):
        wm = self.world()

        if wm.messenger_memory().pass_time() != wm.time() \
            or len(wm.messenger_memory().pass_()) == 0 \
            or wm.messenger_memory().pass_()[0]._receiver != wm.self().unum():

            return False

        self_min = wm.intercept_table().self_reach_cycle()
        intercept_pos = wm.ball().inertia_point(self_min)
        heard_pos = wm.messenger_memory().pass_()[0]._pos

        log.sw_log().team().add_text( f"(sample palyer do heard pass) heard_pos={heard_pos}, intercept_pos={intercept_pos}")

        if not wm.kickable_teammate() \
            and wm.ball().pos_count() <= 1 \
            and wm.ball().vel_count() <= 1 \
            and self_min < 20:
            log.sw_log().team().add_text( f"(sample palyer do heard pass) intercepting!, self_min={self_min}")
            log.debug_client().add_message("Comm:Receive:Intercept")
            Intercept().execute(self)
            self.set_neck_action(NeckTurnToBall())
        else:
            log.sw_log().team().add_text( f"(sample palyer do heard pass) go to point!, cycle={self_min}")
            log.debug_client().set_target(heard_pos)
            log.debug_client().add_message("Comm:Receive:GoTo")

            GoToPoint(heard_pos, 0.5, ServerParam.i().max_dash_power()).execute(self)
            self.set_neck_action(NeckTurnToBall())

        # TODO INTENTION?!?
























