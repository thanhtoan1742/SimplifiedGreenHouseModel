from ModelState import *
from ModelEnvironment import *
from ModelParameter import *
from ModelSetPoint import *
from GreenHouseModel import *
from ODESolver import *

gh = GreenHouseModel()

data_size = 10
time = [i*5 for i in range(data_size)]
