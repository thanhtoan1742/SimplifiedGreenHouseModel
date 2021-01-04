import pandas as pd

from ModelState import *
from ModelEnvironment import *
from ModelParameter import *
from ModelSetPoint import *
from GreenHouseModel import *
from ODESolver import *

DATA_PATH = 'meteo.csv'


def get_data():
    df = pd.read_csv(DATA_PATH)
    df = data[2:-1]

    return df

def run_siciLy_model():
    parameter = ModelParameter(
        h_Air=4.0, h_Gh=4.8,h_Vent=1.6, h_Elevation=104,
        A_Flr=1.3e4, A_Roof=0.2*1.3e4, A_Cov=1.7e4,
        C_Gh_d=0.75, C_Gh_w=0.12,
        c_leakage=1e-4, sigma_InsScr=0.33,
        c_HECin=2.21
    )
    gh = GreenHouseModel(parameter=parameter)
    setPoint = ModelSetPoint(
        U_Blow=0, U_Pad=0, U_ExtCO2=0, 
        U_Fog=0, U_VentForced=0, U_MechCool=0
    )



gh = GreenHouseModel()

data = pd.read_csv(DATA_PATH)