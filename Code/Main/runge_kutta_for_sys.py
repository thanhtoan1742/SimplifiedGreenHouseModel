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

    def runge_kutta_solve(self, t, u_t, h, dx):
        m = u_t.size
        k_1 = np.array([0 for i in range(m)], dtype=float)
        k_2 = np.array([0 for i in range(m)], dtype=float)
        k_3 = np.array([0 for i in range(m)], dtype=float)
        k_4 = np.array([0 for i in range(m)], dtype=float)

        val = dx(t, u_t)
        for i in range(m):
            k_1[i] = h * val[i]

        val = dx(t + h / 2, u_t + 1 / 2 * k_1)
        for i in range(m):
            k_2[i] = h * val[i]

        val = dx(t + h / 2, u_t + 1 / 2 * k_2)
        for i in range(m):
            k_3[i] = h * val[i]

        val = dx(t + h, u_t + k_3)
        for i in range(m):
            k_4[i] = h * val[i]

        u_t_out = u_t + 1 / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
        return u_t_out

    def func_CO2(self, t, u_t):
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
        out_val = self.runge_kutta_solve(0, in_val, h, self.func_CO2)
        next_Model = self.state
        next_Model.update(CO2_Air = out_val[0], CO2_Top = out_val[1])
        return next_Model

# def myFunc(t, x):
#     m = x.size
#     func = np.array([0 for i in range(m)], dtype=float)
#     func[0] = 2 * x[0] + 3 * x[1]
#     func[1] = 3 * x[0] + 2 * x[1]
#     return func

# initial_val = np.array([1.2, 0.3], dtype=float)
# state = ModelState(0,0,0,0,0)
# par = ModelParameter(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
# gh = GreenHouseModel(par)
# setpoint = ModelSetPoint
# environment = ModelEnvironment()
# sv = solver(state, gh, setpoint, environment)

# print(sv.runge_kutta_solve(0,initial_val,0.1,myFunc))