class ModelSetPoint:
    def __init__(self, U_Blow=0, U_Pad=0, U_ExtCO2=0, U_ThScr=0, U_ShScr=0, 
                U_Roof=0, U_Side=0, U_Fog=0, U_VentForced=0, U_MechCool = 0):
        self.U_Blow = U_Blow
        self.U_Pad = U_Pad
        self.U_ExtCO2 = U_ExtCO2
        self.U_ThScr = U_ThScr
        self.U_ShScr = U_ShScr
        self.U_Roof = U_Roof
        self.U_Side = U_Side
        self.U_Fog = U_Fog
        self.U_VentForced = U_VentForced
        self.U_MechCool = U_MechCool
