# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import mean_squared_error


from ModelState import *
from ModelEnvironment import *
from ModelParameter import *
from ModelSetPoint import *
from GreenHouseModel import *
from ODESolver import *

METHOD = 'euler'
NAME = 'sicily'

# %%
DATA_PATH = 'meteo.csv'
REFERENCE_DATA_PATH = 'Greenhouse_climate.csv'

# %%
data = pd.read_csv(DATA_PATH)
data = data[2:-1]
data = data[['Tout', 'Rhout', 'Windsp']]
data.reset_index(inplace=True)

for i in range(len(data)):
    if np.isnan(data['Tout'][i]):
        data['Tout'][i] = data['Tout'][i - 1]

    if np.isnan(data['Rhout'][i]):
        data['Rhout'][i] = data['Rhout'][i - 1]
        
    if np.isnan(data['Windsp'][i]):
        data['Windsp'][i] = data['Windsp'][i - 1]
# data


# %%
ref_data = pd.read_csv(REFERENCE_DATA_PATH)
ref_data = ref_data[2:-1]
ref_data = ref_data[['Tair', 'RHair', 'CO2air']]

ref_data.reset_index(inplace=True)

M_CO2 = 44
for i in range(len(ref_data)):
    if not np.isnan(ref_data['CO2air'][i]):
        ref_data['CO2air'][i] = ref_data['CO2air'][i] * M_CO2 / 24.45 
# ref_data
ref_data['CO2air'].to_csv('CO2air_mg_m-3.csv', index = False)
# %%
def run_Sicily_model():
    parameter = ModelParameter(
        A_Cov=1.7e4, A_Flr=1.3e4, h_Air=4.0, h_Elevation=104, h_Gh=4.8, c_HECin=2.21,
        K_ThScr=0.05e-3,
        A_Roof=0.26*1.3e4, h_Vent=1.6, C_Gh_d=0.75, C_Gh_w=0.12, sigma_InsScr=0.33, c_leakage=1e-4,
    )
    gh = GreenHouseModel(parameter=parameter)
    setpoint = ModelSetPoint(
        U_ThScr=1, U_ShScr=1, U_Roof=0.1, U_Side=1
    )

    state = ModelState(
        CO2_Air=ref_data['CO2air'][0],
        CO2_Top=ref_data['CO2air'][0],
        VP_Air=gh.saturation_VP(ref_data['Tair'][0]),
        VP_Top=gh.saturation_VP(ref_data['Tair'][0]),
    )

    solver = ODESolver(gh)
    result = np.ndarray((len(data), 4))
    result[0] = state.to_numpy_array()

    for i in tqdm(range(0, len(data) - 1)):
        environment = ModelEnvironment(
            T_Out=data['Tout'][i],
            RH_Out=data['Rhout'][i],
            v_Wind=data['Windsp'][i],
            LAI=1.5
        )

        for j in range(60):
            # d_state = gh(setpoint, state, environment)
            # new_state = d_state.to_numpy_array() * 5 + state.to_numpy_array()
            # new_state = ModelState().from_numpy_array(new_state)
            # state = new_state
            # new_state = solver.euler_wrapper_for_GreenHouseModel(state, environment, setpoint, 0, 5)
            if METHOD == 'rk4':
                new_state = solver.rk4_wrapper_for_GreenHouseModel(state, environment, setpoint, 0, 5)
            else :
                new_state = solver.euler_wrapper_for_GreenHouseModel(state, environment, setpoint, 0, 5)
            state = new_state

        # new_state = solver.rk4_wrapper_for_GreenHouseModel(state, environment, setpoint, 0, 300)
        
    
        result[i+1] = state.to_numpy_array()

        if state.CO2_Air < 0 or state.CO2_Top < 0 or state.VP_Air < 0 or state.VP_Top < 0:
            print(f"error at {i}:")
            print(state.to_numpy_array())
            break

        # print(state.to_numpy_array())
        if np.isnan(state.CO2_Air) or np.isnan(state.CO2_Top) or np.isnan(state.VP_Air) or np.isnan(state.VP_Top):
        # if np.isnan(environment.T_Out) or np.isnan(environment.RH_Out) or np.isnan(environment.v_Wind):
            print(f"nan at {i}:")
            print(state.to_numpy_array())
            break
        # new_state = solver.euler_wrapper_for_GreenHouseModel(state, environment, setpoint, 0, 300)
        # result.append(new_state.to_numpy_array())
        # state = new_state
    return result


# %%
result = run_Sicily_model()
res_data = pd.DataFrame(
    result,
    columns=['CO2air', 'CO2top', 'VPair', 'VPtop']
)

# %%

PATH = 'result/' + NAME + '_' + METHOD + '.csv'
res_data.to_csv(PATH, index=False)

# %%
def Cal_rmse(act, predicted):
    for i in range(len(act)):
        if np.isnan(act[i]):
            act[i] = predicted[i]
    return mean_squared_error(act, predicted, squared = False)

#%%

rmse_CO2_Air = Cal_rmse(ref_data['CO2air'], res_data['CO2air'])
print(f'Root mean square error of CO2air: {rmse_CO2_Air}')

#%%
para = ModelParameter()
gh = GreenHouseModel(parameter = para)
ref_VP_Air = [gh.saturation_VP(ref_data['Tair'][i]) for i in range(len(ref_data))]
# ref_VP_Air[0:10]
rmse_VP_Air = Cal_rmse(ref_VP_Air, res_data['VPair'])

print(f'Root mean square error of VPair: {rmse_VP_Air}')

# %%
