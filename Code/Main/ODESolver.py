import numpy as np
from ModelSetPoint import *
from ModelState import *
from ModelEnvironment import *
from GreenHouseModel import *

class ODESolver:

    def __init__(self, gh: GreenHouseModel):
        self.gh = gh
        self.setpoint = None
        self.environment = None

    def rk4_wrapper_for_GreenHouseModel(self, state: ModelState, envir: ModelEnvironment, setPoint: ModelSetPoint, t0, t1):
        u_t = state.to_numpy_array()
        self.environment = envir
        self.setpoint = setPoint
        u_t1 = self.rk4_solver(u_t, t0, t1 - t0, self.du)
        next_state = ModelState()
        next_state.from_numpy_array(u_t1)
        return next_state

    def euler_wrapper_for_GreenHouseModel(self, state: ModelState, envir: ModelEnvironment, setPoint: ModelSetPoint, t0, t1):
        u_t = state.to_numpy_array()
        self.environment = envir
        self.setpoint = setPoint
        u_t1 = self.euler_solver(u_t, t0, t1 - t0, self.du)
        next_state = ModelState()
        next_state.from_numpy_array(u_t1)
        return next_state

    def du(self, u_t, t):
        state = ModelState().from_numpy_array(u_t)
        d_state = self.gh(self.setpoint, state, self.environment)
        return d_state.to_numpy_array()

    def rk4_solver(self, u_t, t, h, du):
        m = len(u_t)
        k_1 = np.array([0 for i in range(m)], dtype=float)
        k_2 = np.array([0 for i in range(m)], dtype=float)
        k_3 = np.array([0 for i in range(m)], dtype=float)
        k_4 = np.array([0 for i in range(m)], dtype=float)

        val = du(u_t, t)
        k_1 = h * val
        # print("k_1= ", k_1)
        val = du(u_t + 1 / 2 * k_1, t + h / 2)
        k_2 = h * val
        # print("k_2= ", k_2)
        val = du(u_t + 1 / 2 * k_2, t + h / 2)
        k_3 = h * val
        # print("k_3= ", k_3)
        val = du(u_t + k_3, t + h)
        k_4 = h * val
        # print("k_4= ", k_4)
        u_t_out = u_t + 1 / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
        # print("u_t= ", u_t_out)
        # print()
        return u_t_out

    def euler_solver(self, u_t, t, h, du):
        return u_t + h * du(u_t, t)