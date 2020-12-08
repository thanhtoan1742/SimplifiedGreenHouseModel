class ModelSetPoint:
    def __init__(self, U_Blow = 1, U_Pad = 1, U_ExtCO2 = 1, 
                U_ThScr = 1, U_ShScr = 1, U_Roof = 1, U_Side = 1):
        self.U_Blow = U_Blow
        self.U_Pad = U_Pad

        #MC_ExtAir
        self.U_ExtCO2 = U_ExtCO2

        #Bach
        self.U_ThScr = U_ThScr
        self.U_ShScr = U_ShScr
        self.U_Roof = U_Roof
        self.U_Side = U_Side