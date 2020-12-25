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

    def runge_kutta_CO2(self, h):
        state = self.state
        in_val = np.array([state.CO2_Air, state.CO2_Top], dtype= float)
        out_val = self.runge_kutta_solve(state.t, in_val, h, self.func_CO2)
        next_Model = self.state
        next_Model.update(CO2_Air = out_val[0], CO2_Top = out_val[1])
        return next_Model


    def euler_solve(self,t,  u_t, h, du):
        return u_t + h * du(t, u_t)

    def euler_CO2(self, h):
        state = self.state
        cur_C02 = np.array([state.CO2_Air, state.CO2_Top], dtype=float)
        next_CO2 = self.euler_solve(state.t, cur_C02, h, self.func_CO2)
        state.update(CO2_Air = next_CO2[0], CO2_Top = next_CO2[1])
        return state


    def func_CO2(self, t, u_t):
        state = ModelState(t, u_t[0], u_t[1], 0, 0)
        gh = self.gh
        setpoint = self.setpoint
        environment = self.environment
        d_CO2_Air, d_CO2_Top = gh(setpoint, state, environment)
        func = np.array([d_CO2_Air, d_CO2_Top], dtype=float)
        return func


def myDx(t, x):
    m = len(x)
    func = np.array([0 for i in range(m)], dtype=float)
    func[0] = x[0] - 2 * x[1] - 2 * np.exp(-t) + 2
    func[1] = 2 * x[0] - x[1] - 2 * np.exp(-t) + 1
    return func

def myFx(t, x):
    print(len(x))
    func = np.array([0 for i in range(len(x))], dtype = float)
    func[0] = np.exp(-t)
    func[1] = 1
    return func

#for checking correctness of rk4 and euler method using customized fx and dx
if __name__ == '__main__':
    initial_val = np.array([1, 1], dtype=float)
    state = ModelState(0,0,0,0,0)
    par = ModelParameter(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    gh = GreenHouseModel(par)
    setpoint = ModelSetPoint()
    environment = ModelEnvironment()
    sv = solver(state, gh, setpoint, environment)

    t = 0
    t_end = 4
    step = 0.01
    rk4 = [initial_val]
    euler = [initial_val]
    true_solution = [initial_val]
    while t < t_end:
        rk4.append(sv.runge_kutta_solve(t, rk4[-1], step, myDx))
        euler.append(sv.euler_solve(t, euler[-1], step, myDx))
        true_solution.append(myFx(t, true_solution[-1]))
        t += step

    for i in range(len(rk4)):
        print("RK4 solution: ", rk4[i], " Euler solution: ", euler[i], " True solution: ", true_solution[i])
