import math

import ModelConstant as constant 
from ModelParameter import *
from ModelSetPoint import *
from ModelState import *
from ModelEnvironment import *

class GreenHouseModel:
    def __init__(self, parameter: ModelParameter):
        self.parameter = parameter
        self.setPoint = None
        self.state = None
        self.environment = None

    def d_CO2_Air(self): #
        cap_CO2_Air = self.cap_CO2_Air()
        # print(f'MC_BlowAir: {self.MV_BlowAir()}, MC_ExtAir: {self.MC_ExtAir()}, MC_PadAir: {self.MC_PadAir()}')
        # print(f'MC_AirCan:{self.MC_AirCan()}, MC_AirTop:{self.MC_AirTop()}, MC_AirOut:{self.MC_AirOut()}, ')
        return (self.MC_BlowAir() + self.MC_ExtAir() + self.MC_PadAir() - self.MC_AirCan() - self.MC_AirTop() - self.MC_AirOut()) / cap_CO2_Air

    def d_CO2_Top(self): #
        cap_CO2_Top = self.cap_CO2_Top()
        return (self.MC_AirTop() - self.MC_TopOut()) / cap_CO2_Top

    def cap_CO2_Air(self): #
        return self.parameter.h_Air

    def cap_CO2_Top(self): #
        return self.parameter.h_Gh - self.parameter.h_Air

    def MC_BlowAir(self): #
        U_Blow = self.setPoint.U_Blow
        if U_Blow == 0:
            return 0

        eta_HeatCO2 = constant.eta_HeatCO2
        P_Blow = self.parameter.P_Blow
        A_Flr = self.parameter.A_Flr

        return (eta_HeatCO2 * U_Blow * P_Blow) / A_Flr

    def MC_ExtAir(self): #
        U_ExtCO2 = self.setPoint.U_ExtCO2
        if U_ExtCO2 == 0:
            return 0

        phi_ExtCO2 = self.parameter.phi_ExtCO2
        A_Flr = self.parameter.A_Flr

        return U_ExtCO2 * phi_ExtCO2 / A_Flr

    def MC_PadAir(self): #
        U_Pad = self.setPoint.U_Pad
        if U_Pad == 0:
            return 0

        phi_Pad = self.parameter.phi_Pad
        A_Flr = self.parameter.A_Flr
        CO2_Out = self.environment.CO2_Out
        CO2_Air = self.state.CO2_Air

        return (U_Pad * phi_Pad) / A_Flr * (CO2_Out - CO2_Air)

    def f_ThScr(self): #
        U_ThScr = self.setPoint.U_ThScr
        rho_Air = self.rho_Air()
        rho_Out = self.rho_Out()
        K_ThScr = self.parameter.K_ThScr
        T_Air = self.T_Air()
        T_Out = self.environment.T_Out
        g = constant.g

        rho_Air_Mean = (rho_Air + rho_Out)/2

        if U_ThScr == 0:
            screen = 0
        else:
            screen = U_ThScr * K_ThScr * math.pow(math.fabs(T_Air-T_Out), 2/3)
        no_screen = (1-U_ThScr)*pow(g*(1-U_ThScr)*math.fabs(rho_Air-rho_Out)/(2*rho_Air_Mean), 1/2)
        # print(f'screen:{screen}, no_screen:{no_screen}')
        return screen + no_screen

    def rho_Out(self):
        M_Air = constant.M_Air
        pressure = 101325 * (1 - 2.5577e-5 * self.parameter.h_Elevation) ** 5.25588
        R = constant.R * 1000
        return M_Air * pressure / ((self.T_Top() + 273.15) * R)

    def rho_Air(self): # should be replace with 3. in Log/note.txt
        rho_Air_0 = constant.rho_Air_0
        g = constant.g
        M_Air = constant.M_Air
        R = constant.R*1000
        h_Elevation = self.parameter.h_Elevation

        return rho_Air_0 * math.exp(g * M_Air * h_Elevation / (293.15 * R))


    def rho_Top(self): # should be replace with 3. in Log/note.txt
        M_Air = constant.M_Air
        T_Top = self.T_Top()
        h_Elevation = self.parameter.h_Elevation
        R = constant.R*1000

        pressure = 101325 * (1 - 2.5577e-5 * h_Elevation) ** 5.25588
        return M_Air * pressure / ((T_Top + 273.15) * R)

    def MC_AirTop(self): #
        CO2_Air = self.state.CO2_Air
        CO2_Top = self.state.CO2_Top
        f_ThScr = self.f_ThScr()
        # print(f'f_ThsScr:{f_ThScr}')
        return f_ThScr*(CO2_Air - CO2_Top)

    def C_d(self): # not safe
        U_ShScr = self.setPoint.U_ShScr
        C_Gh_d = self.parameter.C_Gh_d
        if U_ShScr == 0:
            return C_Gh_d

        eta_ShScrC_d = self.parameter.eta_ShScrC_d

        return C_Gh_d*(1-eta_ShScrC_d*U_ShScr) 

    def C_w(self): # not safe
        U_ShScr = self.setPoint.U_ShScr
        C_Gh_w = self.parameter.C_Gh_w
        if U_ShScr == 0:
            return C_Gh_w

        eta_ShScrC_w = self.parameter.eta_ShScrC_d

        return C_Gh_w*(1 - eta_ShScrC_w*U_ShScr)

    def eta_InsScr(self): #
        sigma_InsScr = self.parameter.sigma_InsScr
        return sigma_InsScr*(2 - sigma_InsScr)

    def f_leakage(self): #
        v_Wind = self.environment.v_Wind
        c_leakage = self.parameter.c_leakage

        if (v_Wind < 0.25):
            return 0.25*c_leakage
        else:
            return v_Wind*c_leakage

    def dd_f_VentRoofSide(self): # not safe, need safety
        U_Roof = self.setPoint.U_Roof
        U_Side = self.setPoint.U_Side
        T_Air = self.T_Air()
        T_Out = self.environment.T_Out
        v_Wind = self.environment.v_Wind
        h_SideRoof = self.parameter.h_SideRoof
        A_Flr = self.parameter.A_Flr
        A_Side = self.parameter.A_Side
        A_Roof = self.parameter.A_Roof
        C_w = self.C_w()
        C_d = self.C_d()
        g = constant.g

        T_Mean_Air = (T_Air + T_Out)/2

        temp1 =  math.pow(U_Roof*U_Side*A_Roof*A_Side, 2) / ( math.pow(U_Roof*A_Roof, 2) + math.pow(U_Side*A_Side, 2) ) 
        temp2 = (2 * g * h_SideRoof * (T_Air-T_Out) ) /(T_Mean_Air + 273.15)
        temp3 = math.pow( (U_Roof*A_Roof + U_Side*A_Side)/2, 2) * C_w*math.pow(v_Wind, 2)
        return (C_d / A_Flr) * math.pow(temp1 * temp2 + temp3, 1/2)

    def dd_f_VentRoof(self): #
        U_Roof = self.setPoint.U_Roof
        if U_Roof == 0:
            return 0

        T_Air = self.T_Air()
        T_Out = self.environment.T_Out
        T_Mean_Air = (T_Air + T_Out)/2
        v_Wind = self.environment.v_Wind
        A_Roof = self.parameter.A_Roof
        A_Flr = self.parameter.A_Flr
        h_Vent = self.parameter.h_Vent
        C_d = self.C_d()
        C_w = self.C_w()
        g = constant.g

        tmp1 = C_d*U_Roof*A_Roof/(2*A_Flr)
        tmp2 = g * h_Vent * (T_Air - T_Out)/(2*(T_Mean_Air + 273.15)) + C_w*pow(v_Wind, 2)
        # print(f'tmp2_1:{g * h_Vent * (T_Air - T_Out)/(2*(T_Mean_Air + 273.15))}, tmp2_2:{C_w*pow(v_Wind, 2)}')
        # print(f'C_w:{C_w}, v_Wind:{v_Wind}')
        # print(f'tmp1:{tmp1}, tmp2:{tmp2}')
        return tmp1*math.pow(tmp2,1/2)

    def dd_f_VentSide(self): #
        U_Side = self.setPoint.U_Side
        if U_Side == 0:
            return 0

        A_Side = self.parameter.A_Side
        v_Wind = self.environment.v_Wind
        A_Flr = self.parameter.A_Flr
        C_d = self.C_d()
        C_w = self.C_w()

        return C_d * U_Side * A_Side * v_Wind * math.pow(C_w, 0.5) / (2 * A_Flr)


    def f_VentRoof(self): # not safe
        U_ThScr = self.setPoint.U_ThScr
        eta_InsScr = self.eta_InsScr()
        dd_f_VentRoof = self.dd_f_VentRoof()
        dd_f_VentRoofSide = self.dd_f_VentRoofSide()
        f_leakage = self.f_leakage()
        eta_Roof = self.parameter.A_Roof/self.parameter.A_Flr
        eta_Roof_Thr = constant.eta_Roof_Thr

        if (eta_Roof >= eta_Roof_Thr):
            return eta_InsScr * dd_f_VentRoof + 0.5*f_leakage
        else:
            # print(f'dd_f_VentRoof:{dd_f_VentRoof}')
            sreen = U_ThScr*dd_f_VentRoof
            no_screen = (1-U_ThScr) * dd_f_VentRoofSide*eta_Roof
            return eta_InsScr*(sreen + no_screen) + 0.5*f_leakage

    def f_VentForced(self): #
        U_VentForced = self.setPoint.U_VentForced
        if U_VentForced == 0:
            return 0

        phi_VentForced = self.parameter.phi_VentForced
        A_Flr = self.parameter.A_Flr
        eta_InsScr = self.eta_InsScr()

        return eta_InsScr * U_VentForced * phi_VentForced / A_Flr

    def f_VentSide(self): # not safe
        U_ThScr = self.setPoint.U_ThScr
        eta_Roof = self.parameter.A_Roof / self.parameter.A_Flr
        eta_Side = self.parameter.A_Side / self.parameter.A_Flr
        eta_InsScr = self.eta_InsScr()
        dd_f_VentSide = self.dd_f_VentSide()
        f_leakage = self.f_leakage()
        dd_f_VentRoofSide = self.dd_f_VentRoofSide()
        eta_Roof_Thr = constant.eta_Roof_Thr

        if eta_Roof >= eta_Roof_Thr:
            return eta_InsScr * dd_f_VentSide + 0.5 * f_leakage
        else:
            return eta_InsScr * (U_ThScr*dd_f_VentSide + (1-U_ThScr)*dd_f_VentRoofSide*eta_Side) +  0.5*f_leakage

    def MC_TopOut(self): #
        f_VentRoof = self.f_VentRoof()
        CO2_Top = self.state.CO2_Top
        CO2_Out = self.environment.CO2_Out
        return f_VentRoof*(CO2_Top - CO2_Out)

    def MC_AirOut(self): #
        f_VentSide = self.f_VentSide()
        f_VentForced = self.f_VentForced()
        CO2_Air = self.state.CO2_Air
        CO2_Out = self.environment.CO2_Out
        # print(f'f_VentSide:{f_VentSide}, f_VentForced:{f_VentForced}')
        return (f_VentSide + f_VentForced) * (CO2_Air - CO2_Out)

    def MC_AirCan(self): #
        M_CH2O = constant.M_CH2O
        H_C_Buf = self.H_C_Buf()
        P = self.P()
        R = self.R()
        # print(f'P:{P}, R:{R}')
        return M_CH2O * H_C_Buf * (P - R)

    def H_C_Buf(self): #
        return 0.5

    def R(self): #
        # R can be simplified to 0
        P = self.P()
        Gamma = self.Gamma()
        CO2_Storm = self.CO2_Storm()
        return P * Gamma / CO2_Storm

    def P(self): #
        Gamma = self.Gamma()
        CO2_Storm = self.CO2_Storm()
        J = self.J()

        return (J/4) * ((CO2_Storm - Gamma)/(CO2_Storm + 2*Gamma))

    def Gamma(self): #
        T_Can = self.T_Can()
        c_Gamma = constant.c_Gamma
        J_MAX_25Leaf = constant.J_MAX_25Leaf
        J_MAX_25Can = self.J_MAX_25Can()

        return T_Can*c_Gamma*(J_MAX_25Leaf/J_MAX_25Can) + 20*c_Gamma*(1 - J_MAX_25Leaf/J_MAX_25Can)

    def CO2_Storm(self): #
        eta_CO2_Storm = constant.eta_CO2_Air_Stom
        CO2_Air = self.state.CO2_Air
        return eta_CO2_Storm * CO2_Air

    def J(self):
        alpha = constant.alpha
        theta = constant.theta
        J_POT = self.J_POT()
        PAR_Can = constant.PAR_Can

        temp1 = J_POT + alpha*PAR_Can
        temp2 = (J_POT + alpha*PAR_Can)**2 - 4*theta*J_POT*alpha*PAR_Can
        return (temp1 - temp2**0.5)/(2*theta)

    def J_POT(self): #
        E_j = constant.E_j
        S = constant.S
        H = constant.H
        R = constant.R
        T_25K = constant.T_25K
        T_CanK = self.T_CanK()
        J_MAX_25Can = self.J_MAX_25Can()

        temp1 = math.exp(E_j*(T_CanK - T_25K)/(R*T_CanK*T_25K))
        temp2 = 1 + math.exp((S*T_25K - H)/(R*T_25K))
        temp3 = 1 + math.exp((S*T_CanK - H)/(R*T_CanK))
        return J_MAX_25Can*temp1*(temp2/temp3)

    # equation 8.20 and 8.1 does not add up in term of units.
    def T_CanK(self): #
        T_Can = self.T_Can()
        return T_Can + 273.15

    def J_MAX_25Can(self): #
        LAI = self.environment.LAI
        J_MAX_25Leaf = constant.J_MAX_25Leaf
        return LAI * J_MAX_25Leaf



#############################################################

    def d_VP_Air(self): #
        return (self.MV_CanAir() + self.MV_PadAir() + self.MV_FogAir() + self.MV_BlowAir() \
            - self.MV_AirThScr() - self.MV_AirTop() - self.MV_AirOut() - self.MV_AirOut_Pad() 
            - self.MV_AirMech()) / self.cap_VP_Air()

    def d_VP_Top(self):
        cap_VP_Top = self.cap_VP_Top()
        return (self.MV_AirTop() - self.MV_TopCov_in() -  self.MV_TopOut()) / cap_VP_Top

    def cap_VP_Air(self): #
        M_Water = constant.M_Water
        R = constant.R*1000
        T_Air = self.T_Air()
        h_Air = self.parameter.h_Air
        return (M_Water * h_Air) / (R*(T_Air + 273.15))

    def cap_VP_Top(self): # similar to cap_VP_Air , line 424 Koidra/climate/state_variable
        # M_Water = constant.M_Water
        # R = constant.R*1000
        # T_Top = self.T_Top()
        # h_Top = self.h_Top()
        # return (M_Water * h_Top) / (R*(T_Top + 273.15))
        return self.cap_VP_Air()

    def VP_Out(self):
        T_Out = self.environment.T_Out
        return self.saturation_VP(T_Out)

    def h_Top(self): #
        h_Air = self.parameter.h_Air
        h_Gh = self.parameter.h_Gh
        return h_Gh - h_Air

    def MV_CanAir(self): #
        T_Can = self.T_Can()
        VP_Air = self.state.VP_Air
        VEC_CanAir = self.VEC_CanAir()
        VP_Can = self.saturation_VP(T_Can)
        return VEC_CanAir * (VP_Can - VP_Air)

    def VEC_CanAir(self): #
        rho_Air = self.rho_Air()
        c_p_Air = constant.c_p_Air
        LAI = self.environment.LAI
        delta_H = constant.delta_H
        gamma = constant.gamma
        r_b = constant.r_b
        r_s = self.r_s()

        return 2*rho_Air*c_p_Air*LAI / (delta_H*gamma* (r_b + r_s))

    def r_s(self): #
        r_s_min = constant.r_s_min
        return r_s_min

    def MV_FogAir(self): # not safe
        U_Fog = self.setPoint.U_Fog
        phi_Fog = self.parameter.phi_Fog
        A_Flr = self.parameter.A_Flr
        return U_Fog*phi_Fog/A_Flr

    def MV_AirThScr(self): #
        s_MV12 = constant.S_MV12
        VP_Air = self.state.VP_Air
        VP_ThScr = self.saturation_VP(self.T_ThScr())
        HEC_AirThScr = self.HEC_AirThScr()
        tmp1 = 1/( 1 + math.exp( s_MV12*(VP_Air - VP_ThScr) ) ) 
        tmp2 = 6.4*1e-9*HEC_AirThScr*(VP_Air-VP_ThScr)
        return tmp1*tmp2

    def HEC_AirThScr(self): #
        U_ThScr = self.setPoint.U_ThScr
        T_Air = self.T_Air()
        T_ThScr = self.T_ThScr()
        return 1.7*U_ThScr*( math.fabs(T_Air - T_ThScr)**0.33 )

    def MV_PadAir(self): # not safe
        rho_Air = self.rho_Air()
        f_Pad = self.f_Pad()
        eta_Pad = self.parameter.eta_Pad
        x_Pad = self.x_Pad()
        x_Out = self.x_Out()
        return rho_Air * f_Pad * (eta_Pad * (x_Pad - x_Out) + x_Out)

    # fan-pad pull air from outside (Out) to inside (Air)
    # So, x_Pad can be calculated as x_Air
    def x_Pad(self):
        return self.x_Air()

    # Assume that the air inside the green house is saturated
    # parital pressure of air is equivalent to vapour pressure
    def x_Air(self):
        VP_Air = self.state.VP_Air
        return self.specific_humidity(VP_Air)

    def x_Out(self):
        T_Out = self.environment.T_Out
        RH_Out = self.environment.RH_Out
        VP_Out = self.saturation_VP(T_Out)
        
        partial_pressure = RH_Out * VP_Out
        return self.specific_humidity(partial_pressure)

    def MV_BlowAir(self): # not safe
        eta_HeatVap = constant.eta_HeatVap
        U_Blow = self.setPoint.U_Blow
        P_Blow = self.parameter.P_Blow
        A_Flr = self.parameter.A_Flr

        return (eta_HeatVap * U_Blow * P_Blow) / A_Flr

    def MV_AirTop(self): #
        f_ThScr = self.f_ThScr()
        M_Water = constant.M_Water
        R = constant.R*1000
        VP_Air = self.state.VP_Air
        VP_Top = self.state.VP_Top
        T_Air = self.T_Air()
        T_Top = self.T_Top()
        return M_Water * f_ThScr / R * (VP_Air / (T_Air + 273.15) - VP_Top / (T_Top + 273.15))

    def MV_AirOut(self): # f_VentSide not safe
        f_AirOut = self.f_VentSide() + self.f_VentForced()
        M_Water = constant.M_Water
        R = constant.R*1000
        VP_Air = self.state.VP_Air
        VP_Out = self.VP_Out()
        T_Air = self.T_Air()
        T_Out = self.environment.T_Out
        return M_Water * f_AirOut / R * (VP_Air / (T_Air + 273.15) - VP_Out / (T_Out + 273.15))

    def MV_AirOut_Pad(self): # f_Pad not safe
        f_Pad = self.f_Pad()
        M_Water = constant.M_Water
        R = constant.R*1000
        VP_Air = self.state.VP_Air
        T_Air = self.T_Air()
        return f_Pad * M_Water / R * (VP_Air / (T_Air + 273.15))

    def f_Pad(self): # not safe
        U_Pad = self.setPoint.U_Pad
        if U_Pad == 0:
            return 0

        phi_Pad = self.parameter.phi_Pad
        A_Flr = self.parameter.A_Flr
        return U_Pad*phi_Pad/A_Flr

    def MV_AirMech(self): #
        VP_Air = self.state.VP_Air
        VP_MechCool = self.saturation_VP(self.T_MechCool())
        HEC_MechAir = self.HEC_MechAir()
        S_MV12 = constant.S_MV12
        res = 1 / (1 + math.exp(S_MV12 * (VP_Air - VP_MechCool))) * 6.4 * 1e-9
        res = res * HEC_MechAir * (VP_Air - VP_MechCool)
        return res

    def HEC_MechAir(self): # not safe
        U_MechCool = self.setPoint.U_MechCool
        COP_MechCool = self.parameter.COP_MechCool
        P_MechCool = self.parameter.P_MechCool
        A_Flr = self.parameter.A_Flr
        T_Air = self.T_Air()
        T_MechCool = self.T_MechCool()
        VP_Air = self.state.VP_Air
        VP_MechCool = self.saturation_VP(T_MechCool)
        delta_H = constant.delta_H
        res = U_MechCool * COP_MechCool * P_MechCool / A_Flr
        res = res / (T_Air - T_MechCool + 6.4 * 1e-9 * delta_H * (VP_Air - VP_MechCool))
        return res

    def MV_TopOut(self): #
        M_Water = constant.M_Water
        R = constant.R*1000
        f_VentRoof = self.f_VentRoof()
        VP_Top = self.state.VP_Top
        VP_Out = self.VP_Out()
        T_Top = self.T_Top()
        T_Out = self.environment.T_Out
        return M_Water/R * f_VentRoof*(VP_Top / (T_Top + 273.15) - VP_Out / (T_Out + 273.15))

    def MV_TopCov_in(self): #
        VP_Top = self.state.VP_Top
        VP_Cov_in = self.saturation_VP(self.T_Cov_in())
        HEC_TopCov_in = self.HEC_TopCov_in()
        S_MV12 = constant.S_MV12

        # print()
        # print(self.T_Cov_in())
        # print(VP_Top)
        # print(VP_Cov_in)
        # print(HEC_TopCov_in)
        # print(S_MV12)
        res = 1 / (1 + math.exp(S_MV12 * (VP_Top - VP_Cov_in))) * 6.4 * 1e-9
        res = res * HEC_TopCov_in * (VP_Top - VP_Cov_in)


        return res
    
    # Buck's formula
    def saturation_VP(self, temp): #
        pressure = 0.61121 * math.exp((18.678 - (temp/234.5)) * (temp/(257.14 + temp))) # this is in kPa
        return pressure*1000 # converto to Pa

    # def saturation_VP(self, t):
    #     return 610.78 * math.exp(17.27 * t / (t +237.3))
    # Vaisala eq:14
    def specific_humidity(self, partial_pressure):
        M_Water = constant.M_Water
        M_Air = constant.M_Air
        P_Ambient = constant.P_Ambient

        return (M_Water/M_Air)*(partial_pressure/(P_Ambient - partial_pressure))
    
    def HEC_TopCov_in(self): #
        c_HECin = self.parameter.c_HECin
        T_Top = self.T_Top()
        T_Cov_in = self.T_Cov_in()
        A_Cov = self.parameter.A_Cov
        A_Flr = self.parameter.A_Flr
        return c_HECin * ((T_Top - T_Cov_in) ** 0.33) * A_Cov / A_Flr

    def T_Air(self):
        T_Out = self.environment.T_Out
        return T_Out + 3

    def T_Top(self):
        T_Out = self.environment.T_Out
        return T_Out + 2

    def T_Can(self):
        T_Out = self.environment.T_Out
        return T_Out + 1

    def T_ThScr(self):
        T_Out = self.environment.T_Out
        return T_Out + 1

    def T_Cov_in(self):
        T_Out = self.environment.T_Out
        return T_Out + 1

    def T_MechCool(self):
        T_Out = self.environment.T_Out
        return T_Out + 1

    def __call__(self, setPoint: ModelSetPoint, state: ModelState, environment: ModelEnvironment):
        self.setPoint = setPoint
        self.state = state
        self.environment = environment

        return ModelState(self.d_CO2_Air(), self.d_CO2_Top(), self.d_VP_Air(), self.d_VP_Top())

###USE WHEN TESTING METHODS###
# if __name__ == "__main__": 
#     model = CO2_Model(0,0)
#     model.MC_AirTop(1,1,1,1,1,1,1)
