# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd

from ModelState import *
from ModelEnvironment import *
from ModelParameter import *
from ModelSetPoint import *
from GreenHouseModel import *
from ODESolver import *


# %%
DATA_PATH = 'meteo.csv'
REFERENCE_DATA_PATH = 'Greenhouse_climate.csv'


# %%
data = pd.read_csv(DATA_PATH)
data = data[2:-1]
data = data[['Tout', 'Rhout', 'Windsp']]
data


# %%
ref_data = pd.read_csv(REFERENCE_DATA_PATH)
ref_data = ref_data[2:-1]
ref_data = ref_data[['Tair', 'RHair', 'CO2air']]
ref_data


# %%
def run_Sicily_model():
    parameter = ModelParameter(
        A_Cov=1.7e4, A_Flr=1.3e4, h_Air=4.0, h_Elevation=104, h_Gh=4.8, c_HECin=2.21,
        A_Roof=0.2*1.3e4, h_Vent=1.6, C_Gh_d=0.75, C_Gh_w=0.12, sigma_InsScr=0.33, c_leakage=1e-4,
    )
    gh = GreenHouseModel(parameter=parameter)
    setpoint = ModelSetPoint(
        U_ThScr=1, U_ShScr=1, U_Roof=1, U_Side=1
    )

    environment = ModelEnvironment(
        T_Out=17.7,
        RH_Out=87.8,
        v_Wind=3.2,
        LAI=1.5
    )

    state = ModelState(
        CO2_Air=484,
        CO2_Top=484,
        VP_Air=gh.saturation_VP(20.2),
        VP_Top=gh.saturation_VP(20.2),
    )

    d_state = gh(setpoint, state, environment)
    new_state = d_state.to_numpy_array() + state

run_Sicily_model()

# %%
