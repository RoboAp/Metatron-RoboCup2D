from lib.action.go_to_point import GoToPoint
from lib.action.intercept import Intercept
from lib.action.neck_scan_players import NeckScanPlayers
from lib.action.neck_turn_to_ball import NeckTurnToBall
from lib.action.neck_turn_to_ball_or_scan import NeckTurnToBallOrScan
from lib.action.scan_field import ScanField
from lib.action.smart_kick import SmartKick
from lib.debug.debug import log
from lib.rcsc.server_param import ServerParam

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.player.player_agent import PlayerAgent


class BhvGoToBallAndKick:
    def execute(self, agent: 'PlayerAgent'):
        wm = agent.world()
        sp = ServerParam.i()

        if not wm.ball().pos_valid():
            log.debug_client().add_message('minimal_scan_ball')
            agent.set_neck_action(NeckTurnToBallOrScan())
            return ScanField().execute(agent)

        if wm.self().is_kickable():
            target = sp.their_team_goal_pos()
            first_speed = sp.ball_speed_max()

            log.debug_client().set_target(target)
            log.debug_client().add_message('minimal_kick_to_goal')

            SmartKick(target, first_speed, first_speed * 0.8, 3).execute(agent)
            agent.set_neck_action(NeckScanPlayers())
            return True

        log.debug_client().set_target(wm.ball().pos())
        log.debug_client().add_message('minimal_go_to_ball')

        if Intercept().execute(agent):
            agent.set_neck_action(NeckTurnToBall())
            return True

        dist_thr = max(0.5, wm.self().player_type().kickable_area() * 0.5)
        if GoToPoint(wm.ball().pos(), dist_thr, sp.max_dash_power()).execute(agent):
            agent.set_neck_action(NeckTurnToBall())
            return True

        agent.set_neck_action(NeckTurnToBallOrScan())
        return True
