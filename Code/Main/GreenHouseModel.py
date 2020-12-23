import math

import ModelConstant as constant 
from ModelParameter import *
from ModelSetPoint import *
from ModelState import *

class GreenHouseModel:
    def __init__(self, parameter: ModelParameter):
        self.parameter = parameter
        self.setPoint = None
        self.state = None
        self.environment = None
        

    def d_CO2_Air(self):
        cap_CO2_Air = self.parameter.cap_CO2_Air
        return (self.MC_BlowAir() + self.MC_ExtAir() + self.MC_PadAir() - self.MC_AirCan() - self.MC_AirTop() - self.MC_AirOut()) / cap_CO2_Air

    def d_CO2_Top(self):
        cap_CO2_Top = self.parameter.cap_CO2_Top
        return (self.MC_AirTop() - self.MC_TopOut()) / cap_CO2_Top

        ###___DUY-FUNC____###
    def MC_BlowAir(self):
        eta_HeatCO2 = constant.eta_HeatCO2
        U_Blow = self.setPoint.U_Blow
        P_Blow = self.parameter.P_Blow
        A_Flr = self.parameter.A_Flr
        return (eta_HeatCO2 * U_Blow * P_Blow) / A_Flr

    def MC_ExtAir(self):
        U_ExtCO2 = self.setPoint.U_ExtCO2
        phi_ExtCO2 = self.parameter.phi_ExtCO2
        A_Flr = self.parameter.A_Flr
        return U_ExtCO2 * phi_ExtCO2 / A_Flr

    def MC_PadAir(self):
        U_Pad = self.setPoint.U_Pad
        phi_Pad = self.parameter.phi_Pad
        A_Flr = self.parameter.A_Flr
        CO2_Out = self.environment.CO2_Out
        CO2_Air = self.state.CO2_Air
        return (U_Pad * phi_Pad) / A_Flr * (CO2_Out - CO2_Air)

    def MC_AirCan(self):
        M_CH2O = constant.M_CH2O
        H_C_Buf = self.H_C_Buf()
        P = self.P()
        R = self.R()
        return  M_CH2O * H_C_Buf * (P - R)

    def R(self):
        P = self.P()
        C_ComP = constant.C_ComP
        CO2_Air_Stom = constant.CO2_Air_Stom
        ComP = C_ComP * self.parameter.T_Can
        CO2_Stom = CO2_Air_Stom * self.state.CO2_Air
        return P * ComP / CO2_Stom

    def H_C_Buf(self):
        C_Buf = self.parameter.C_Buf
        C_Max_Buf = constant.C_Max_Buf
        if C_Buf > C_Max_Buf: return 0
        return 1
    ###___END_DUY_FUNC___###

    ###__START-BACH-FUNCS__###
    def f_ThScr(self): 
        p_Air = self.parameter.p_Air
        p_Top = self.parameter.p_Top
        K_ThScr = self.parameter.K_ThScr
        U_ThScr = self.setPoint.U_ThScr
        T_Air = self.environment.T_Air
        T_Top = self.environment.T_Top
        g = constant.g

        p_Air_Mean = (p_Air + p_Top)/2

        screen = U_ThScr * K_ThScr * math.pow(math.fabs(T_Air-T_Top), 2/3)
        no_screen = (1-U_ThScr)*pow( g*(1-U_ThScr)*math.fabs(p_Air-p_Top)/(2*p_Air_Mean), 1/2)
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
        return C_Gh_d*(1-eta_ShScrC_d*U_ShScr) 

    def C_w(self):
        U_ShScr = self.setPoint.U_ShScr
        eta_ShScrC_w = self.parameter.eta_ShScrC_d
        C_Gh_w = self.parameter.C_Gh_w
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
        eta_InsScr = self.eta_InsScr()
        dd_f_VentRoof = self.dd_f_VentRoof()
        dd_f_VentRoofSide = self.dd_f_VentRoofSide()
        f_leakage = self.f_leakage()
        U_ThScr = self.setPoint.U_ThScr

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

    ###__END-BACH-FUNCS__###

    ###NGUYEN

    # REDECLARATION OF BACH'S FUNC
    # def f_leakage(self, v_Wind):
    #     if v_Wind < 0.25:
    #         return 0.25 * self.c_leakage
    #     else:
    #         return v_Wind * self.c_leakage
    # def C_d(self, U_ShSc):
    #     return self.C_Gh_d * (1 - self.eta_ShScrCd * U_ShSc)
    #
    # def C_w(self, U_ShSc):
    #     return self.C_Gh_w * (1 - self.eta_ShScrCd * U_ShSc)
    #
    # def eta_InsScr(self):
    #     return self.sigma_InsScr * (2 - self.sigma_InsScr)
    #
    # def dd_f_VentRoofSide(self, T_Out, T_Air, U_Roof, U_Side, U_ShSc, v_Wind):
    #     T_MeanAir = T_Out + T_Air
    #     op1 = math.pow(self.A_Roof * self.A_Side * U_Roof * U_Side, 2) / (
    #                 math.pow(self.A_Roof * U_Roof, 2) + math.pow(self.A_Side * U_Side, 2))
    #     op2 = 2 * self.g * self.h_SideRoof * (T_Air - T_Out) / (T_MeanAir + 273.15)
    #     op3 = math.pow(self.A_Roof * U_Roof + self.A_Side * U_Side, 2) * self.C_w(U_ShSc) * math.pow(v_Wind, 2) / 4
    #
    #     return self.C_d(U_ShSc) / self.A_Flr * math.pow(op1 * op2 + op3, 0.5)
    
    def dd_f_VentSide(self):
        C_d = self.C_d()
        C_w = self.C_w()

        U_Side = self.setPoint.U_Side
        A_Side = self.parameter.A_Side
        v_Wind = self.parameter.v_Wind
        A_Flr = self.parameter.A_Flr

        return C_d * U_Side * A_Side * v_Wind * math.pow(C_w, 0.5) / (2 * A_Flr)

    def f_VentForced(self):
        eta_InsScr = self.eta_InsScr()

        U_VentForced = self.setPoint.U_VentForced
        phi_VentForced = self.parameter.phi_VentForced
        A_Flr = self.parameter.A_Flr

        return eta_InsScr * U_VentForced * phi_VentForced / A_Flr

    def f_VentSide(self):
        eta_Roof = self.parameter.A_Roof / self.parameter.A_Flr
        eta_Side = self.parameter.A_Side / self.parameter.A_Flr
        U_ThScr = self.setPoint.U_ThScr

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

#############################################################################################

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

    
#############################################################################################

    def __call__(self, setPoint: ModelSetPoint, state: ModelState, environment: ModelEnvironment):
        self.setPoint = setPoint
        self.state = state
        self.environment = environment

        return self.d_CO2_Air(), self.d_CO2_Top()

###USE WHEN TESTING METHODS###
# if __name__ == "__main__": 
#     model = CO2_Model(0,0)
#     model.MC_AirTop(1,1,1,1,1,1,1)