# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from tqdm import tqdm

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
data.reset_index(inplace=True)
# data


# %%
ref_data = pd.read_csv(REFERENCE_DATA_PATH)
ref_data = ref_data[2:-1]
ref_data = ref_data[['Tair', 'RHair', 'CO2air']]
ref_data.reset_index(inplace=True)
# ref_data

# %%
def run_Sicily_model():
    parameter = ModelParameter(
        A_Cov=1.7e4, A_Flr=1.3e4, h_Air=4.0, h_Elevation=104, h_Gh=4.8, c_HECin=2.21,
        K_ThScr=0.05e-3,
        A_Roof=0.2*1.3e4, h_Vent=1.6, C_Gh_d=0.75, C_Gh_w=0.12, sigma_InsScr=0.33, c_leakage=1e-4,
    )
    gh = GreenHouseModel(parameter=parameter)
    setpoint = ModelSetPoint(
        U_ThScr=1, U_ShScr=1, U_Roof=1, U_Side=1
    )

    state = ModelState(
        CO2_Air=ref_data['CO2air'][0],
        CO2_Top=ref_data['CO2air'][0],
        VP_Air=gh.saturation_VP(ref_data['Tair'][0]),
        VP_Top=gh.saturation_VP(ref_data['Tair'][0]),
    )

    solver = ODESolver(gh)
    result = [state.to_numpy_array()]

    for i in range(0, len(data) - 1):
        environment = ModelEnvironment(
            T_Out=data['Tout'][i],
            RH_Out=data['Rhout'][i],
            v_Wind=data['Windsp'][i],
            LAI=1.5
        )


        for j in range(60):
            d_state = gh(setpoint, state, environment)
            new_state = d_state.to_numpy_array() * 5 + state.to_numpy_array()
            new_state = ModelState().from_numpy_array(new_state)
            state = new_state

        # d_state = gh(setpoint, state, environment)
        # new_state = d_state.to_numpy_array() * 300 + state.to_numpy_array()
        # new_state = ModelState().from_numpy_array(new_state)
        # state = new_state

        print(d_state.to_numpy_array())
        print(new_state.to_numpy_array())
        print()
        # new_state = solver.euler_wrapper_for_GreenHouseModel(state, environment, setpoint, 0, 300)
        # result.append(new_state.to_numpy_array())
        # state = new_state

    return result
    


result = run_Sicily_model()
print(result)

# %%
len(ref_data)
# %%
