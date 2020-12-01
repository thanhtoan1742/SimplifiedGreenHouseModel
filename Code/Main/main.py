from CO2_Model import CO2_Model

dx = CO2_Model(cap_CO2_Air = 1, cap_CO2_Top = 1)

print(dx.evaluate(0, 0, 0))
