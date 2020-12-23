class ModelState:
    def __init__(self, t, CO2_Air, CO2_Top, VP_Air, VP_Top):
        self.t = t
        self.CO2_Air = CO2_Air
        self.CO2_Top = CO2_Top
        self.VP_Air = VP_Air
        self.VP_Top = VP_Top

    def update(self, t=None, CO2_Air=None, CO2_Top=None, VP_Air=None, VP_Top=None):
        if t is not None:
            self.t = t
        if CO2_Air is not None:
            self.CO2_Air = CO2_Air
        if CO2_Top is not None:
            self.CO2_Top = CO2_Top
        if VP_Air is not None:
            self.VP_Air = VP_Air
        if VP_Top is not None:
            self.VP_Top = VP_Top