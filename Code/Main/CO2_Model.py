class CO2_Model:
    def __init__(self):
        self.CO2_Air_0 = 0
        self.CO2_Top_0 = 0
        self.t = 0
        
    def d_CO2_Air(self):
        return self.MC_BlowAir() + self.MC_ExtAir() + self.MC_PadAir() - self.MC_AirCan() - self.MC_AirTop() - self.MC_AirOut()

    def d_CO2_Top(self):
        return self.MC_AirTop() - self.MC_TopOut()

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
    
    def evaluate(self, CO2_Air_0, CO2_Top_0, t):
        self.CO2_Air_0 = CO2_Air_0
        self.CO2_Top_0 = CO2_Top_0
        self.t = t

        return self.d_CO2_Air(), self.d_CO2_Top()
