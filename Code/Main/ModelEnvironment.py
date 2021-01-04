import numpy as np

class ModelEnvironment:
    def __init__(self, CO2_Out=0, T_Out = 0, RH_Out = 0, v_Wind = 0, LAI = 0):
        self.CO2_Out = CO2_Out # data
        self.T_Out = T_Out # data
        self.RH_Out = RH_Out # data
        self.v_Wind = v_Wind # data
        self.LAI = LAI # Vanthoor page 31

    def to_numpy_array(self):
        return np.array([
            self.CO2_Out,
            self.T_Out,
            self.RH_Out,
            self.v_Wind, 
            self.LAI, 
        ], dtype=float)
        
    def from_numpy_array(self, arr):
        self.CO2_Out = arr[0]
        self.T_Out = arr[1]
        self.RH_Out = arr[2]
        self.v_Wind = arr[3]
        self.LAI = arr[4]
