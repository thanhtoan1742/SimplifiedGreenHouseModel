class ModelSetPoint:
    def __init__(self, U_Blow=1, U_Pad=1, U_ExtCO2=1, U_ThScr=1, U_ShScr=1, 
                U_Roof=1, U_Side=1, U_Fog=1, U_VentForced=1, U_MechCool = 1):
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

    def update(self, U_Blow=None, U_Pad=None, U_ExtCO2=None, U_ThScr=None, U_ShScr=None, 
                U_Roof=None, U_Side=None, U_Fog=None, U_VentForced=None, U_MechCool = None):
        if U_Blow is not None:
            self.U_Blow = U_Blow
        if U_Pad is not None:
            self.U_Pad = U_Pad
        if U_ExtCO2 is not None:
            self.U_ExtCO2 = U_ExtCO2
        if U_ThScr is not None:
            self.U_ThScr = U_ThScr
        if U_ShScr is not None:
            self.U_ShScr = U_ShScr
        if U_Roof is not None:
            self.U_Roof = U_Roof
        if U_Side is not None:
            self.U_Side = U_Side
        if U_Fog is not None:
            self.U_Fog = U_Fog
        if U_VentForced is not None:
            self.U_VentForced = U_VentForced
        if U_MechCool is not None:
            self.U_MechCool = U_MechCool