from pyrusgeom.geom_2d import Vector2D
from lib.rcsc.server_param import ServerParam as SP

class formation:
    def __init__(self):
        self.sp = SP.i()

    def get_target(self, wm) -> Vector2D:
        num_jog = wm.self().unum()
        pos_bola = wm.ball().pos()
        
        tm_min = min(wm.intercept_table().teammate_reach_cycle(), wm.intercept_table().self_reach_cycle())
        op_min = wm.intercept_table().opponent_reach_cycle()

        if tm_min + 2 < op_min:
            if num_jog in [2, 3, 4]: 
                x_base = -20.0 
            elif num_jog in [5, 6, 7, 8]: 
                x_base = 0.0  
            elif num_jog in [9, 10, 11]:
                x_base = 25.0
        else:
            if num_jog in [2, 3, 4]: 
                x_base = -40.0 
            elif num_jog in [5, 6, 7, 8]: 
                x_base = -25.0 
            elif num_jog in [9, 10, 11]: 
                x_base = -10.0

        # fator de atração da bola
        fator_x = 0.3
        x_jog = x_base + (pos_bola.x() * fator_x)

        # Trava para zagueiros não subirem ao ataque
        if num_jog in [2, 3, 4] and x_jog > 0.0:
            x_jog = 0.0

        y_mapa = {2: -15, 3: 0, 4: 15, 5: -20, 6: -7, 7: 7, 8: 20, 9: -15, 10: 0, 11: 15}
        y_jog = y_mapa.get(num_jog, 0)
        y_jog += (pos_bola.y() * 0.3)

        return Vector2D(x_jog, y_jog)
