import math

class CO2_Model:
    def __init__(self, cap_CO2_Air, cap_CO2_Top):
        self.cap_CO2_Air = cap_CO2_Air
        self.cap_CO2_Top = cap_CO2_Top

        self.CO2_Air_0 = 0
        self.CO2_Top_0 = 0
        self.t = 0
        
    def d_CO2_Air(self):
        return (self.MC_BlowAir() + self.MC_ExtAir() + self.MC_PadAir() - self.MC_AirCan() - self.MC_AirTop() - self.MC_AirOut()) / self.cap_CO2_Air

    def d_CO2_Top(self):
        return (self.MC_AirTop() - self.MC_TopOut()) / self.cap_CO2_Top

    def MC_BlowAir(self):
        return 0

    def MC_ExtAir(self):
        return 0

    def MC_PadAir(self):
        return 0

    def MC_AirCan(self):
        return 0

    def MC_AirTop(self):
        return 0

    def MC_AirOut(self):
        return 0

    def MC_TopOut(self):
        return 0    

#############################################################################################

    def P(self):
        return quadraticSolver(self.Res, 
            self.CO2_Air_0 + self.CO2_O5() + self.Res*self.P_Max(),
            self.CO2_Air_0*self.P_Max()
        ) 
    
    def quadraticSolver(self, a, b, c):
        delta =  b * b - 4 * a * c
        if delta < 0:
            pass
        elif delta == 0:
            return -b / 2 * a
        else:
            return (-b + math.sqrt(delta) / 2 * a)

    def CO2_05(self):
        return self.CO2_Air_0 - 0.5 * self.Res * self.P_Max()

    def P_Max(self):
        return (self.P_MLT + self.P_Max_Single() * self.L()) / (self.L() + self.L_05())

    def L(self):
        return self.L_0 * (1 - (self.K * math.exp(-self.K * self.LAI)) / (1 - self.m))

    def L_05(self):
        return 2 * self.P_MLT * self.L() - self.L()

    def P_Max_Single(self):
        return self.k() * self.f()

    def k(self):
        return self.LAI * self.k_T_opt * math.exp(-self.H_a * (self.T_opt - self.T_0) / (self.R * self.T_opt * self.T_0))

    def f(self):
        return (1 + math.exp((-self.H_d ** 2 + self.T_opt * self.S) / (self.R * self.H_d * self.T_opt))) / (1 + math.exp((-self.H_d ** 2 + self.T_0 * self.S) / (self.R * self.H_d * self.T_0)))

    
#############################################################################################

    def evaluate(self, CO2_Air_0, CO2_Top_0, t):
        self.CO2_Air_0 = CO2_Air_0
        self.CO2_Top_0 = CO2_Top_0
        self.t = t

        return self.d_CO2_Air(), self.d_CO2_Top()
