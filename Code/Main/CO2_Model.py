class CO2_Model:
    def __init__(self):
        self.CO2_Air_0 = 0
        self.CO2_Top_0 = 0
        self.t = 0
        
    def d_CO2_Air(self):
        return 0

    def d_CO2_Top(self):
        return 0
    
    def evaluate(self, CO2_Air_0, CO2_Top_0, t):
        self.CO2_Air_0 = CO2_Air_0
        self.CO2_Top_0 = CO2_Top_0
        self.t = t

        return self.d_CO2_Air(), self.d_CO2_Top()
