class ModelEnvironment:
    def __init__(self, CO2_Out=0, VP_Out=0, T_Air=0, T_Top=0, T_Can=0, T_Out=0, C_Buf=0):
        self.CO2_Out = CO2_Out
        self.VP_Out = VP_Out
        self.T_Air = T_Air
        self.T_Top = T_Top
        self.T_Can = T_Can
        self.T_Out = T_Out
        self.C_Buf = C_Buf # state variable of tomato model in VAN11

    def update(self, CO2_Out=None, VP_Out=None, T_Air=None, T_Top=None, T_Out=None):
        if CO2_Out is not None:
            self.CO2_Out = CO2_Out
        if VP_Out is not None:
            self.VP_Out = VP_Out
        if T_Air is not None:
            self.T_Air = T_Air
        if T_Top is not None:
            self.T_Top = T_Top
        if T_Out is not None:
            self.T_Out = T_Out
