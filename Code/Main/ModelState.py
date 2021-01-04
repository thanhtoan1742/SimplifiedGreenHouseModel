import numpy as np

class ModelState:
    def __init__(self, CO2_Air=None, CO2_Top=None, VP_Air=None, VP_Top=None):
        self.CO2_Air = CO2_Air
        self.CO2_Top = CO2_Top
        self.VP_Air = VP_Air
        self.VP_Top = VP_Top

    def to_numpy_array(self):
        return np.array([self.CO2_Air, self.CO2_Top, self.VP_Air, self.VP_Top], dtype=float)

    def from_numpy_array(self, arr):
        self.CO2_Air = arr[0]
        self.CO2_Top = arr[1]
        self.VP_Air = arr[2]
        self.VP_Top = arr[2]

    def __add__(self, other):
        return ModelState().from_numpy_array(self.to_numpy_array() + other.to_numpy_array())

    def __mul__(self, other):
        return ModelState().from_numpy_array(self.to_numpy_array()*other)

    def __str__(self):
        return 'ass'