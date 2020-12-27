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

    def rk4_wrapper(self, state: ModelState, envir: ModelEnvironment, setpoint: ModelSetPoint, t0, t1):
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
        print("k_1= ", k_1)
        val = du(u_t + 1 / 2 * k_1, t + h / 2)
        for i in range(m):
            k_2[i] = h * val[i]
        print("k_2= ", k_2)
        val = du(u_t + 1 / 2 * k_2, t + h / 2)
        for i in range(m):
            k_3[i] = h * val[i]
        print("k_3= ", k_3)
        val = du(u_t + k_3, t + h)
        for i in range(m):
            k_4[i] = h * val[i]
        print("k_4= ", k_4)
        u_t_out = u_t + 1 / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
        print("u_t= ", u_t_out)
        print()
        return u_t_out

    def euler_solver(self, u_t, t, h, du):
        return u_t + h * du(u_t, t)


<<<<<<< HEAD:Code/Main/ode_solver.py
def myDx(x, t):
=======
#for checking correctness of rk4 and euler method using customized fx and dx
def myDx(t, x):
>>>>>>> a9c09cdd5830005bc0f8bee2eeed19c0a3bd2658:Code/Main/ODESolver.py
    m = len(x)
    func = np.array([0 for i in range(m)], dtype=float)
    func[0] = x[0] - 2 * x[1] - 2 * np.exp(-t) + 2
    func[1] = 2 * x[0] - x[1] - 2 * np.exp(-t) + 1
    return func

def myFx(x, t):
    func = np.array([0 for i in range(len(x))], dtype = float)
    func[0] = np.exp(-t) * np.sin(t)
    func[1] = np.exp(-t) * np.cos(t)
    return func

if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    state = ModelState(0,0,0,0)
    par = ModelParameter(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    gh = GreenHouseModel(par)
    setpoint = ModelSetPoint()
    environment = ModelEnvironment()
<<<<<<< HEAD:Code/Main/ode_solver.py
    sv = solver(gh)
=======
    sv = ODESolver(state, gh, setpoint, environment)
>>>>>>> a9c09cdd5830005bc0f8bee2eeed19c0a3bd2658:Code/Main/ODESolver.py

    initial_val = np.array([1, 1], dtype=float)
    t = 0
    t_end = 0.5
    step = 0.1
    rk4 = [initial_val]
    euler = [initial_val]
    true_solution = [initial_val]
    while t < t_end:
        rk4.append(sv.rk4_solver(rk4[-1], t, step, myDx))
        euler.append(sv.euler_solver(euler[-1], t, step, myDx))
        true_solution.append(myFx(true_solution[-1], t))
        t += step



