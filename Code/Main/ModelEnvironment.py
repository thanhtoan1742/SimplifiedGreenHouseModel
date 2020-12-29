class ModelEnvironment:
    def __init__(self, CO2_Out=0, VP_Out=0, T_opt=0, T_Air=0, T_Top=0, T_Can=0, T_Out=0, 
                T_Cov_in = 0, C_Buf=0, T_MechCool = 0, T_ThSrc = 0, x_Pad = 0, x_Out = 0):
        self.CO2_Out = CO2_Out
        self.VP_Out = VP_Out
        self.T_opt = T_opt
        self.T_Air = T_Air
        self.T_Top = T_Top
        self.T_Can = T_Can
        self.T_Out = T_Out
        self.T_Cov_in = T_Cov_in
        self.T_MechCool = T_MechCool
        self.T_ThSrc = T_ThSrc 
        self.C_Buf = C_Buf # state variable of tomato model in VAN11
        self.x_Pad = x_Pad
        self.x_Out = x_Out

    def update(self, CO2_Out=None, VP_Out=None, T_opt=None, T_Air=None, T_Top=None, T_Out=None, 
                T_Can = None, T_Cov_in = None, T_MechCool = None, T_ThSrc = None, x_Pad = None, 
                x_Out = None):
        if CO2_Out is not None:
            self.CO2_Out = CO2_Out
        if VP_Out is not None:
            self.VP_Out = VP_Out
        if T_opt is not None:
            self.T_opt = T_opt
        if T_Air is not None:
            self.T_Air = T_Air
        if T_Top is not None:
            self.T_Top = T_Top
        if T_Can is not None:
            self.T_Can = T_Can
        if T_Out is not None:
            self.T_Out = T_Out
        if T_Cov_in is not None:
            self.T_Cov_in = T_Cov_in
        if T_MechCool is not None:
            self.T_MechCool = T_MechCool
        if T_ThSrc is not None:
            self.T_ThSrc = T_ThSrc
        if x_Pad is not None:
            self.x_Pad = x_Pad
        if x_Out is not None:
            self.x_Out = x_Out
