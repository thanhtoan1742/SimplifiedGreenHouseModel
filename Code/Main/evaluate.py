# %%
import numpy as np
from numpy.core.function_base import linspace
import pandas as pd
from statistics import mean
from sklearn.metrics import mean_squared_error
from GreenHouseModel import GreenHouseModel
import matplotlib.pyplot as plt

METHOD = 'rk4' # euler | rk4
NAME = 'Arizona' # sicily | Arizona | Netherlan | Texas
DATA_PATH = 'meteo.csv'
REFERENCE_DATA_PATH = 'Greenhouse_climate.csv'
PREDICTED_DATA_PATH = 'result/' + NAME + '_' + METHOD + '.csv'
RESULT_DATA_PATH = 'result/rrmse_' + NAME + '_' + METHOD + '.txt'
FIGURE_PATH = 'result/' + NAME + '_' + METHOD + '.png'
# %%
gh = GreenHouseModel(parameter=None)
# %%
ref_data = pd.read_csv(REFERENCE_DATA_PATH)
ref_data = ref_data[2:-1]
ref_data = ref_data[['Tair', 'RHair', 'CO2air']]

ref_data.reset_index(inplace=True)

M_CO2 = 44
ref_data['CO2air'] = ref_data['CO2air'] * M_CO2 / 24.45 

ref_data['VPair'] = [gh.saturation_VP(e) for e in ref_data['Tair'].to_numpy()]
# %%
pred_data = pd.read_csv(PREDICTED_DATA_PATH)

# %%
def rrmse(true, predicted):
    for i in range(len(true)):
        if np.isnan(true[i]):
            true[i] = predicted[i]

    rmse = mean_squared_error(true, predicted, squared=False)
    rrmse = (100/mean(true))*rmse
    return rrmse
# %%
CO2_Air_RRMSE = rrmse(ref_data['CO2air'].to_numpy(), pred_data['CO2air'].to_numpy())
VP_Air_RRMSE = rrmse(ref_data['VPair'].to_numpy(), pred_data['VPair'].to_numpy())
# %%
print(CO2_Air_RRMSE)
print(VP_Air_RRMSE)

# %%
with open(RESULT_DATA_PATH, 'w+') as f:
    file_content = ''

    file_content += 'relative root mean squared error of CO2air: ' + str(CO2_Air_RRMSE) + '%\n'
    file_content += 'relative root mean squared error of VPair: ' + str(VP_Air_RRMSE) + '%\n'

    f.write(file_content)
# %%
y_true = ref_data['CO2air'].to_numpy()
y_pred = pred_data['CO2air'].to_numpy()

plt.plot(y_true)
plt.plot(y_pred)
plt.savefig(FIGURE_PATH)
# %%

# %%
