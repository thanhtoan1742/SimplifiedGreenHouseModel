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

    def MC_AirCan(self): #
        M_CH2O = constant.M_CH2O
        H_C_Buf = self.H_C_Buf()
        P = self.P()
        R = self.R()
        return  M_CH2O * H_C_Buf * (P - R)

    def R(self): #
        # R got simplified to 0
        # return 0
        C_gamma = constant.C_gamma
        eta_CO2_Air_Stom = constant.eta_CO2_Air_Stom
        T_Can = self.environment.T_Can
        CO2_Air = self.state.CO2_Air
        P = self.P()

        gamma = C_gamma * T_Can
        CO2_Stom = eta_CO2_Air_Stom * CO2_Air
        return P * gamma / CO2_Stom

    def H_C_Buf(self): #
        C_Buf = self.environment.C_Buf
        C_Max_Buf = constant.C_Max_Buf

        if C_Buf > C_Max_Buf: 
            return 0
        return 1

    def f_ThScr(self): 
        U_ThScr = self.setPoint.U_ThScr
        # if U_ThScr == 0:
        #     return 0

        rho_Air = self.parameter.rho_Air
        rho_Top = self.parameter.rho_Top
        K_ThScr = self.parameter.K_ThScr
        T_Air = self.environment.T_Air
        T_Top = self.environment.T_Top
        g = constant.g

        rho_Air_Mean = (rho_Air + rho_Top)/2

        screen = U_ThScr * K_ThScr * math.pow(math.fabs(T_Air-T_Top), 2/3)
        no_screen = (1-U_ThScr)*pow( g*(1-U_ThScr)*math.fabs(rho_Air-rho_Top)/(2*rho_Air_Mean), 1/2)
        return screen + no_screen

    def MC_AirTop(self):
        CO2_Air = self.state.CO2_Air
        CO2_Top = self.state.CO2_Top
        f_ThScr = self.f_ThScr()
        return f_ThScr*(CO2_Air - CO2_Top)

    def C_d(self):
        U_ShScr = self.setPoint.U_ShScr
        eta_ShScrC_d = self.parameter.eta_ShScrC_d
        C_Gh_d = self.parameter.C_Gh_d

        if U_ShScr == 0:
            return C_Gh_d

        return C_Gh_d*(1-eta_ShScrC_d*U_ShScr) 

    def C_w(self):
        U_ShScr = self.setPoint.U_ShScr
        eta_ShScrC_w = self.parameter.eta_ShScrC_d
        C_Gh_w = self.parameter.C_Gh_w

        if U_ShScr == 0:
            return C_Gh_w

        return C_Gh_w*(1 - eta_ShScrC_w*U_ShScr)

    def dd_f_VentRoofSide(self):
        U_Roof = self.setPoint.U_Roof
        U_Side = self.setPoint.U_Side
        T_Air = self.environment.T_Air
        T_Out = self.environment.T_Out
        v_Wind = self.parameter.v_Wind
        h_SideRoof = self.parameter.h_SideRoof
        A_Flr = self.parameter.A_Flr
        A_Side = self.parameter.A_Side
        A_Roof = self.parameter.A_Roof
        C_w = self.C_w()
        C_d = self.C_d()
        g = constant.g

        T_Mean_Air = (T_Air + T_Out)/2

        T_diff_1 =  math.pow(U_Roof*U_Side*A_Roof*A_Side, 2) / ( math.pow(U_Roof*A_Roof, 2) + math.pow(U_Side*A_Side, 2) ) 
        T_diff_2 = (2 * g * h_SideRoof * (T_Air-T_Out) ) /T_Mean_Air
        P_diff = math.pow( (U_Roof*A_Roof + U_Side*A_Side)/2, 2) * C_w*math.pow(v_Wind, 2)
        return (C_d / A_Flr) * math.pow(T_diff_1 * T_diff_2 + P_diff, 1/2)

    def f_leakage(self):
        v_Wind = self.parameter.v_Wind
        c_leakage = self.parameter.c_leakage

        if (v_Wind < 0.25):
            return 0.25*c_leakage
        else:
            return v_Wind*c_leakage

    def dd_f_VentRoof(self):
        U_Roof = self.setPoint.U_Roof
        T_Air = self.environment.T_Air
        T_Out = self.environment.T_Out
        v_Wind = self.parameter.v_Wind
        A_Roof = self.parameter.A_Roof
        A_Flr = self.parameter.A_Flr
        h_Vent = self.parameter.h_Vent

        C_d = self.C_d()
        C_w = self.C_w()

        g = constant.g

        T_Mean_Air = (T_Air + T_Out)/2

        tmp1 = C_d*U_Roof*A_Roof/(2*A_Flr)

        tmp2 = g * h_Vent * (T_Air - T_Out)/(2*T_Mean_Air) + C_w*pow(v_Wind, 2) 
        return tmp1*pow(tmp2,1/2)

    def eta_InsScr(self):
        sigma_InsScr = self.parameter.sigma_InsScr
        return sigma_InsScr*(2 - sigma_InsScr)

    def f_VentRoof(self):
        U_ThScr = self.setPoint.U_ThScr
        eta_InsScr = self.eta_InsScr()
        dd_f_VentRoof = self.dd_f_VentRoof()
        dd_f_VentRoofSide = self.dd_f_VentRoofSide()
        f_leakage = self.f_leakage()

        eta_Roof = self.parameter.A_Roof/self.parameter.A_Flr

        eta_Roof_Thr = constant.eta_Roof_Thr

        if (eta_Roof >= eta_Roof_Thr):
            return eta_InsScr * dd_f_VentRoof() + 0.5*f_leakage
        else:
            tmp1 = U_ThScr*dd_f_VentRoof
            tmp2 = (1-U_ThScr) * dd_f_VentRoofSide*eta_Roof
            return eta_InsScr*(tmp1 + tmp2) + 0.5*f_leakage

    def MC_TopOut(self):
        f_VentRoof = self.f_VentRoof()
        CO2_Air = self.state.CO2_Air
        CO2_Top = self.state.CO2_Top
        return f_VentRoof*(CO2_Air - CO2_Top)

    def dd_f_VentSide(self):
        U_Side = self.setPoint.U_Side
        if U_Side == 0:
            return 0

        A_Side = self.parameter.A_Side
        v_Wind = self.parameter.v_Wind
        A_Flr = self.parameter.A_Flr
        C_d = self.C_d()
        C_w = self.C_w()

        return C_d * U_Side * A_Side * v_Wind * math.pow(C_w, 0.5) / (2 * A_Flr)

    def f_VentForced(self):
        U_VentForced = self.setPoint.U_VentForced
        if U_VentForced == 0:
            return 0

        phi_VentForced = self.parameter.phi_VentForced
        A_Flr = self.parameter.A_Flr
        eta_InsScr = self.eta_InsScr()

        return eta_InsScr * U_VentForced * phi_VentForced / A_Flr

    def f_VentSide(self):
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
            return eta_InsScr * (U_ThScr * dd_f_VentSide +
                                   (1 - U_ThScr) * dd_f_VentRoofSide * eta_Side) + \
                   0.5 * f_leakage

    def MC_AirOut(self):
        f_VentSide = self.f_VentSide()
        f_VentForced = self.f_VentForced()

        CO2_Air = self.state.CO2_Air
        CO2_Out = self.environment.CO2_Out
        return (f_VentSide + f_VentForced) * (CO2_Air - CO2_Out)

    def P(self):
        Res = self.parameter.Res
        CO2_Air = self.state.CO2_Air
        CO2_05 = self.CO2_05()
        P_Max = self.P_Max()

        return self.quadraticSolver(Res, CO2_Air + CO2_05 + Res*P_Max, CO2_Air*P_Max) 
    
    def quadraticSolver(self, a, b, c):
        delta = b*b - 4*a*c
        # TODO: clarify the solution of this equation.
        if delta < 0:
            pass
        elif delta == 0:
            return -b / (2*a)
        else:
            return ((-b + math.sqrt(delta)) / (2*a))

    def CO2_05(self):
        CO2_Air = self.state.CO2_Air
        Res = self.parameter.Res
        P_Max = self.P_Max()

        return CO2_Air - 0.5*Res*P_Max

    def P_Max(self):
        P_MLT = self.parameter.P_MLT
        P_Max_Single = self.P_Max_Single()
        L = self.L()
        L_05 = self.L_05()

        return (P_MLT + P_Max_Single*L) / (L + L_05)

    def L(self):
        L_0 = self.parameter.L_0
        K = self.parameter.K
        LAI = self.parameter.LAI
        m = self.parameter.m
        
        return L_0*(1 - K*math.exp(-K*LAI)/(1 - m))

    def L_05(self):
        P_MLT = self.parameter.P_MLT
        L = self.L()

        return 2*P_MLT*L - L

    def P_Max_Single(self):
        k = self.k()
        f = self.f()
        return k * f

    def k(self):
        T_opt = self.parameter.T_opt
        k_T_opt = self.parameter.k_T_opt
        LAI = self.parameter.LAI
        T_Air = self.environment.T_Air
        H_a = self.parameter.H_a

        R_Const = constant.R_Const

        return LAI * k_T_opt * math.exp(-H_a * (T_opt - T_Air) / (R_Const * T_opt * T_Air))

    # R_const in ModelConstant (discriminate with R() respiratory func in MCCanAir)
    def f(self):
        H_d = self.parameter.H_d
        S = self.parameter.S
        T_opt = self.parameter.T_opt
        T_Air = self.environment.T_Air

        R_Const = constant.R_Const

        return (1 + math.exp((-H_d ** 2 + T_opt * S) / (R_Const * -H_d * T_opt))) / (1 + math.exp((-H_d ** 2 + T_Air * S) / (R_Const * H_d * T_Air)))

#############################################################

    def d_VP_Air(self):
        return (self.MV_CanAir() + self.MV_PadAir() + self.MV_FogAir() + self.MV_BlowAir() \
            - self.MV_AirThScr() - self.MV_AirTop() - self.MV_AirOut() - self.MV_AirOut_Pad() 
            - self.MV_AirMech) / self.cap_VP_Air()

    def d_VP_Top(self):
        cap_VP_Top = self.cap_VP_Top()
        return (self.MV_AirTop() - self.MV_TopCov_in() -  self.MV_TopOut()) / cap_VP_Top

    def cap_VP_Air(self):
        M_H2O = constant.M_H2O
        R = constant.R
        T_Air = self.environment.T_Air
        h_Air = self.parameter.h_Air
        return (M_H2O * h_Air) / (R*(T_Air + 273.15))

    def cap_VP_Top(self):
        M_H2O = constant.M_H2O
        R = constant.R
        T_Air = self.environment.T_Air
        h_Top = self.h_Top()
        return (M_H2O * h_Top) / (R*(T_Air + 273.15))

    def h_Top(self):
        h_Air = self.parameter.h_Air
        h_Gh = self.parameter.h_Gh
        return (h_Air + h_Gh) / 2

    def MV_CanAir(self):
        VEC_CanAir = self.VEC_CanAir()
        VP_Can = self.saturation_VP(self.environment.T_Can)
        VP_Air = self.saturation_VP(self.environment.T_Air)
        return VEC_CanAir * (VP_Can - VP_Air)

    def VEC_CanAir(self):
        rho_Air = self.parameter.rho_Air
        c_p_Air = constant.c_p_Air
        LAI = self.parameter.LAI
        delta_H = constant.delta_H
        gamma = constant.gamma
        r_b = constant.r_b
        r_s = self.r_s()
        return 2*rho_Air*c_p_Air*LAI / (delta_H*gamma* (r_b - r_s))

    def r_s(self):
        r_s_min = constant.r_s_min
        rf_R = self.rf('R')
        rf_CO2 = self.rf('CO2')
        rf_VP = self.rf('VP')
        return r_s_min*rf_R*rf_CO2*rf_VP
    
    def rf(self, mode):
        if mode == 'R':
            R_Can = constant.R_Can
            c_evap1 = constant.c_evap1
            c_evap2 = constant.c_evap2
            return (R_Can + c_evap1)/(R_Can + c_evap2)
        elif mode == 'CO2':
            c_evap3 = self.c_evap3()
            eta_mg_ppm = constant.eta_mg_ppm
            CO2_Air = self.state.CO2_Air
            return 1 + c_evap3*( (eta_mg_ppm*CO2_Air-200)**2 )
        else:
            return 1 + self.evap4()*( (self.VP_Can() - self.VP_Air())**2 )

    def evap3(self):
        c_day_evap3 = constant.c_day_evap3
        c_night_evap3 = constant.c_night_evap3
        S_r_s = self.S_r_s()
        return c_day_evap3*(1-S_r_s) + c_night_evap3*S_r_s

    def evap4(self):
        c_day_evap4 = constant.c_day_evap4
        c_night_evap4 = constant.c_night_evap4
        S_r_s = self.S_r_s()
        return c_day_evap4*(1-S_r_s) + c_night_evap4*S_r_s

    def S_r_s(self):
        s_r_s = constant.s_r_s
        R_Can_SP = constant.R_Can_SP
        R_Can = constant.R_Can
        return 1/ ( 1 + math.exp(s_r_s* (R_Can - R_Can_SP) ) ) 

    def MV_FogAir(self):
        U_Fog = self.setPoint.U_Fog
        phi_Fog = self.parameter.phi_Fog
        A_Flr = self.parameter.A_Flr
        return U_Fog*phi_Fog/A_Flr

    def MV_AirThScr(self):
        s_MV12 = constant.S_MV12
        VP_Air = self.state.VP_Air
        VP_ThScr = self.saturation_VP(self.environment.T_ThScr)
        HEC_AirThScr = self.HEC_AirThScr()
        tmp1 = 1/( 1 + math.exp( s_MV12*(VP_Air - VP_ThScr) ) ) 
        tmp2 = 6.4*1e-9*HEC_AirThScr*(VP_Air-VP_ThScr)
        return tmp1*tmp2

    def HEC_AirThScr(self): 
        U_ThScr = self.setPoint.U_ThScr
        T_Air = self.environment.T_Air 
        T_ThScr = self.environment.T_ThScr
        return 1.7*U_ThScr*( math.fabs(T_Air - T_ThScr)**0.33 )

    def MV_PadAir(self):
        rho_Air = self.parameter.rho_Air
        f_Pad = self.f_Pad()
        eta_Pad = self.parameter.eta_Pad
        x_Pad = self.environment.x_Pad
        x_Out = self.environment.x_Out
        return rho_Air * f_Pad * (eta_Pad * (x_Pad - x_Out) + x_Out)

    def MV_BlowAir(self):
        eta_HeatVap = constant.eta_HeatVap
        U_Blow = self.setPoint.U_Blow
        P_Blow = self.parameter.P_Blow
        A_Flr = self.parameter.A_Flr

        return (eta_HeatVap * U_Blow * P_Blow) / A_Flr

    def MV_AirThSrc(self):
        VP_Air = self.state.VP_Air
        VP_ThScr = self.saturation_VP(self.environment.T_ThSrc)
        HEC_ThScr = self.HEC_ThSrc()
        S_MV12 = constant.S_MV12
        res = 1 / (1 + math.exp(S_MV12 * (VP_Air - VP_ThScr))) * 6.4 * 1e-9
        res = res * HEC_ThScr * (VP_Air - VP_ThScr)
        return res

    def HEC_ThSrc(self):
        U_ThScr = self.setPoint.U_ThScr
        T_Air = self.environment.T_Air
        T_ThSrc = self.environment.T_ThSrc
        return 1.7 * U_ThScr * (abs(T_Air - T_ThSrc) ** 0.33)

    def MV_AirTop(self):
        f_ThScr = self.f_ThScr()
        M_H2O = constant.M_H2O
        R = constant.R
        VP_Air = self.state.VP_Air
        VP_Top = self.state.VP_Top
        T_Air = self.environment.T_Air
        T_Top = self.environment.T_Top
        return M_H2O * f_ThScr / R * (VP_Air / (T_Air + 273.15) - VP_Top / (T_Top + 273.15))

    def MV_AirOut(self):
        f_AirOut = self.f_VentSide() + self.f_VentForced()
        M_H2O = constant.M_H2O
        R = constant.R
        VP_Air = self.state.VP_Air
        VP_Out = self.parameter.VP_Out
        T_Air = self.environment.T_Air
        T_Out = self.environment.T_Out
        return M_H2O * f_AirOut / R * (VP_Air / (T_Air + 273.15) - VP_Out / (T_Out + 273.15))

    def MV_AirOut_Pad(self):
        f_Pad = self.f_Pad()
        M_H2O = constant.M_H2O
        R = constant.R
        VP_Air = self.state.VP_Air
        T_Air = self.environment.T_Air
        return f_Pad * M_H2O / R * (VP_Air / (T_Air + 273.15))

    def MV_AirMech(self):
        VP_Air = self.state.VP_Air
        VP_MechCool = self.saturation_VP(self.environment.T_MechCool)
        HEC_MechAir = self.HEC_MechAir()
        S_MV12 = constant.S_MV12
        res = 1 / (1 + math.exp(S_MV12 * (VP_Air - VP_MechCool))) * 6.4 * 1e-9
        res = res * HEC_MechAir * (VP_Air - VP_MechCool)
        return res

    def HEC_MechAir(self):
        U_MechCool = self.setPoint.U_MechCool
        COP_MechCool = self.parameter.COP_MechCool
        P_MechCool = self.parameter.P_MechCool
        A_Flr = self.parameter.A_Flr
        T_Air = self.environment.T_Air
        T_MechCool = self.environment.T_MechCool
        VP_Air = self.state.VP_Air
        VP_MechCool = self.saturation_VP(T_MechCool)
        delta_H = constant.delta_H
        res = U_MechCool * COP_MechCool * P_MechCool / A_Flr
        res = res / (T_Air - T_MechCool + 6.4 * 1e-9 * delta_H * (VP_Air - VP_MechCool))
        return res

    def MV_TopOut(self):
        M_H2O = constant.M_H2O
        R = constant.R
        f_VentRoof = self.f_VentRoof()
        VP_Top = self.state.VP_Top
        VP_Out = self.environment.VP_Out
        T_Top = self.environment.T_Top
        T_Out = self.environment.T_Out
        return M_H2O * R * f_VentRoof(VP_Top / (T_Top + 273.15) - VP_Out / (T_Out + 273.15))

    def MV_TopCov_in(self):
        VP_Top = self.state.VP_Top
        VP_Cov_in = self.saturation_VP(self.environment.T_Cov_in)
        HEC_TopCov_in = self.HEC_TopCov_in()
        S_MV12 = constant.S_MV12
        res = 1 / (1 + math.exp(S_MV12 * (VP_Top - VP_Cov_in))) * 6.4 * 1e-9
        res = res * HEC_TopCov_in * (VP_Top - VP_Cov_in)
        return res
    
    def saturation_VP(self, temp):
        return 610.78 * math.exp(temp / (temp + 238.3) * 17.2694)
    
    def HEC_TopCov_in(self):
        c_HECin = self.parameter.c_HECin
        T_Top = self.environment.T_Top
        T_Cov_in = self.environment.T_Cov_in
        A_Cov = self.parameter.A_Cov
        A_Flr = self.parameter.A_Flr
        return c_HECin * ((T_Top - T_Cov_in) ** 0.33) * A_Cov / A_Flr

    def __call__(self, setPoint: ModelSetPoint, state: ModelState, environment: ModelEnvironment):
        self.setPoint = setPoint
        self.state = state
        self.environment = environment

        return ModelState(CO2_Air=self.d_CO2_Air(), CO2_Top=self.d_CO2_Top())

###USE WHEN TESTING METHODS###
# if __name__ == "__main__": 
#     model = CO2_Model(0,0)
#     model.MC_AirTop(1,1,1,1,1,1,1)