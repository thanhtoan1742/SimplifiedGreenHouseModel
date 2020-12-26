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

    def rk4__wrapper(self, state: ModelState, envir: ModelEnvironment, setpoint: ModelSetPoint, t0, t1):
        u_t = state.to_numpy_array()
        self.environment = envir
        self.setpoint = setpoint
        u_t1 = self.rk4_solver(u_t, t0, t1 - t0, self.du)
        next_state = ModelState()
        next_state.from_numpy_array(u_t1)
        return next_state

    def euler_wrapper(self, state: ModelState, envir: ModelEnvironment, setPoint: ModelSetPoint, t0, t1):
        u_t = state.to_numpy_array()
        self.environment = envir
        self.setpoint = setpoint
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
        for i in range(m):
            k_1[i] = h * val[i]

        val = du(u_t + 1 / 2 * k_1, t + h / 2)
        for i in range(m):
            k_2[i] = h * val[i]

        val = du(u_t + 1 / 2 * k_2, t + h / 2)
        for i in range(m):
            k_3[i] = h * val[i]

        val = du(u_t + k_3, t + h)
        for i in range(m):
            k_4[i] = h * val[i]

        u_t_out = u_t + 1 / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
        return u_t_out

    def euler_solver(self, u_t, t, h, du):
        return u_t + h * du(u_t, t)


def myDx(t, x):
    m = len(x)
    func = np.array([0 for i in range(m)], dtype=float)
    func[0] = - x[0] + x[1]
    func[1] = - x[0] - x[1]
    return func

def myFx(t, x):
    func = np.array([0 for i in range(len(x))], dtype = float)
    func[0] = np.exp(-t) * np.sin(t)
    func[1] = np.exp(-t) * np.cos(t)
    return func

#for checking correctness of rk4 and euler method using customized fx and dx
if __name__ == '__main__':

    state = ModelState(0,0,0,0,0)
    par = ModelParameter(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    gh = GreenHouseModel(par)
    setpoint = ModelSetPoint()
    environment = ModelEnvironment()
    sv = ODESolver(state, gh, setpoint, environment)

    initial_val = np.array([0, 1], dtype=float)
    t = 0
    t_end = 10
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
