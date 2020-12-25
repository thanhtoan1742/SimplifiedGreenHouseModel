import numpy as np
from ModelSetPoint import *
from ModelState import *
from ModelEnvironment import *
from GreenHouseModel import *
    
class solver:

    def __init__(self, state : ModelState, gh : GreenHouseModel, setpoint : ModelSetPoint, environment : ModelEnvironment ):
        self.state = state
        self.gh = gh
        self.setpoint = setpoint
        self.environment = environment

    def runge_kutta_solve(self, t, u_t, m, h, dx):
        k_1 = np.array([0 for i in range(m)], dtype=float)
        k_2 = np.array([0 for i in range(m)], dtype=float)
        k_3 = np.array([0 for i in range(m)], dtype=float)
        k_4 = np.array([0 for i in range(m)], dtype=float)
        for i in range(m):
            k_1[i] = h * dx(t, u_t, m)[i]
        for i in range(m):
            k_2[i] = h * dx(t + h / 2, u_t + 1 / 2 * k_1, m)[i]
        for i in range(m):
            k_3[i] = h * dx(t + h / 2, u_t + 1 / 2 * k_2, m)[i]
        for i in range(m):
            k_4[i] = h * dx(t + h, u_t + k_3, m)[i]
        u_t_out = u_t + 1 / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
        return u_t_out

    def func_CO2(self, t, u_t, m):
        state = ModelState(0, u_t[0], u_t[1], 0, 0)
        gh = self.gh
        setpoint = self.setpoint
        environment = self.environment
        d_CO2_Air, d_CO2_Top = gh(setpoint, state, environment)
        func = np.array([d_CO2_Air, d_CO2_Top], dtype=float)
        return func

    def runge_kutta_CO2(self, h):
        state = self.state
        in_val = np.array([state.CO2_Air, state.CO2_Top], dtype= float)
        out_val = self.runge_kutta_solve(0, in_val, 2, h, self.func_CO2)
        next_Model = self.state
        next_Model.update(CO2_Air = out_val[0], CO2_Top = out_val[1])
        return next_Model

