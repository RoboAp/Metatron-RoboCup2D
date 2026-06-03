from base import goalie_decision
from base.strategy_formation import StrategyFormation
from base.set_play.bhv_set_play import Bhv_SetPlay
from base.bhv_go_to_ball_and_kick import BhvGoToBallAndKick
from lib.debug.debug import log
from lib.rcsc.types import GameModeType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from lib.player.world_model import WorldModel
    from lib.player.player_agent import PlayerAgent


# TODO TACKLE GEN
# TODO GOAL KICK L/R
# TODO GOAL L/R
def get_decision(agent: 'PlayerAgent'):
    wm: 'WorldModel' = agent.world()
    st = StrategyFormation().i()
    st.update(wm)

    if wm.self().goalie():
        if goalie_decision.decision(agent):
            return True

    if wm.game_mode().type() != GameModeType.PlayOn:
        if Bhv_SetPlay().execute(agent):
            return True

    log.sw_log().team().add_text(f'is kickable? dist {wm.ball().dist_from_self()} '
                                 f'ka {wm.self().player_type().kickable_area()} '
                                 f'seen pos count {wm.ball().seen_pos_count()} '
                                 f'is? {wm.self()._kickable}')
    return BhvGoToBallAndKick().execute(agent)
