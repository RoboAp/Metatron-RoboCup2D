from lib.player.player_agent import PlayerAgent
from lib.action.neck_turn_to_ball import NeckTurnToBall

class treino(PlayerAgent):
    def action_impl(self):
        wm = self.world()
        numero = wm.self().unum()
        estado = str(wm.game_mode().type())
        
        if 'BeforeKickOff' in estado or 'Goal' in estado:
            posicoes_343 = {
                1: (-48.0, 0.0),    
                2: (-30.0, -15.0), 3: (-30.0, 0.0), 4: (-30.0, 15.0),
                5: (-15.0, -20.0), 6: (-15.0, -6.0), 7: (-15.0, 6.0), 8: (-15.0, 20.0),
                9: (-2.0, -15.0), 10: (-0.5, 0.0), 11: (-2.0, 15.0)
            }
            if numero in posicoes_343:
                x, y = posicoes_343[numero]
                self.do_move(x, y) 
                
        self.set_neck_action(NeckTurnToBall())
        return
