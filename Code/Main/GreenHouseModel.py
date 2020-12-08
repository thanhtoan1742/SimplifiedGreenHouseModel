import math

from ModelConstant import  *
from ModelParameter import *
from ModelSetPoint import *
from ModelState import *

class GreenHouseModel:
    def __init__(self, parameter: ModelParameter):
        self.parameter = parameter
        self.setPoint = ModelSetPoint()
        self.state = ModelState()
        

    def d_CO2_Air(self):
        return (self.MC_BlowAir() + self.MC_ExtAir() + self.MC_PadAir() - self.MC_AirCan() - self.MC_AirTop() - self.MC_AirOut()) / self.cap_CO2_Air

    def d_CO2_Top(self):
        return (self.MC_AirTop() - self.MC_TopOut()) / self.cap_CO2_Top

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
        CO2_Out = self.parameter.CO2_Out
        CO2_Air = self.state.CO2_Air
        return (U_Pad * phi_Pad) / A_Flr * (CO2_Out - CO2_Air)

    def MC_AirCan(self):
        M_CH2O = M_CH2O
        H_C_Buf = self.H_C_Buf()
        P = self.P()
        R = self.R(P)
        return M_CH2O * H_C_Buf * (P - R)

    def R(self, P):
        ComP = C_ComP * self.parameter.T_Can
        CO2_Stom = CO2_Air_Stom * self.state.CO2_Air
        return P * ComP / CO2_Stom

    def H_C_Buf(self):
        C_Buf = self.parameter.C_Buf
        C_Max_Buf = C_Max_Buf
        if C_Buf > C_Max_Buf: return 0
        return 1
    ###___END_DUY_FUNC___###

    ###__START-BACH-FUNCS__###
    def f_ThScr(self): 
        p_Air = self.parameter.p_Air
        p_Top = self.parameter.p_Top
        K_ThScr = self.parameter.K_ThScr
        U_ThScr = self.setPoint.U_ThScr
        T_Air = self.state.T_Air
        T_Top = self.state.T_Top

        p_Air_Mean = (p_Air + p_Top)/2

        screen = U_ThScr * K_ThScr * math.pow(math.fabs(T_Air-T_Top), 2/3)
        no_screen = (1-U_ThScr)*pow( g*(1-U_ThScr)*math.fabs(p_Air-p_Top)/(2*p_Air_Mean), 1/2)
        return screen + no_screen

    def MC_AirTop(self):
        CO2_Air = self.state.CO2_Air
        CO2_Top = self.state.Co2_Top
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
        T_Air = self.parameter.T_Air
        T_Out = self.parameter.T_Out
        v_Wind = self.parameter.v_Wind
        h_SideRoof = self.parameter.h_SideRoof
        A_Flr = self.parameter.A_Flr
        A_Side = self.parameter.A_Side
        A_Roof = self.parameter.A_Roof
        C_w = self.C_w()
        C_d = self.C_d()

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
        T_Air = self.state.T_Air
        T_Out = self.parameter.T_Out
        v_Wind = self.parameter.v_Wind
        A_Roof = self.parameter.A_Roof
        A_Flr = self.parameter.A_Flr
        h_Vent = self.parameter.h_Vent

        C_d = self.C_d()
        C_w = self.C_w()

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
    
    def dd_f_VentSide(self, U_Side, U_ShSc, v_Wind):
        return self.dd_f_VentRoofSide(0, U_Side, 0, 0, U_ShSc, v_Wind)

    def f_VentForced(self, U_VentForced):
        return self.eta_InsScr() * U_VentForced * self.phi_VentForced / self.A_Flr

    def f_VentSide(self, eta_Roof, eta_Side, T_Out, T_Air, U_Roof, U_Side, U_ThScr, U_ShSc, v_Wind):
        if eta_Roof >= self.eta_RoofThr:
            return self.eta_InsScr() * self.dd_f_VentSide(U_Side, U_ShSc, v_Wind) + 0.5 * self.f_leakage(v_Wind)
        else:
            return self.eta_InsScr() * (U_ThScr * self.dd_f_VentSide(U_Side, U_ShSc, v_Wind) +
                                   (1 - U_ThScr) * self.dd_f_VentRoofSide(T_Out, T_Air, U_Roof, U_Side, U_ShSc, v_Wind) * eta_Side) + \
                   0.5 * self.f_leakage(v_Wind)

    def MC_AirOut(self, eta_Roof, eta_Side, T_Out, T_Air, U_Roof, U_Side, U_ThScr, U_ShSc, v_Wind,
                  U_VentForced, CO2_Air, CO2_Out):
        return (self.f_VentSide(eta_Roof, eta_Side, T_Out, T_Air, U_Roof, U_Side, U_ThScr, U_ShSc, v_Wind) +
                self.f_VentForced(U_VentForced)) * (CO2_Air - CO2_Out)
    ###END_NGUYEN

#############################################################################################

    def P(self):
        return self.quadraticSolver(
            self.parameter.Res, 
            self.state.CO2_Air + self.CO2_O5() + self.parameter.Res * self.P_Max(),
            self.state.CO2_Air * self.P_Max()
        ) 
    
    def quadraticSolver(self, a, b, c):
        delta =  b * b - 4 * a * c
        if delta < 0:
            pass
        elif delta == 0:
            return -b / 2 * a
        else:
            return (-b + math.sqrt(delta) / 2 * a)

    def CO2_05(self):
        return self.CO2_Air_0 - 0.5 * self.Res * self.P_Max()

    def P_Max(self):
        return (self.P_MLT + self.P_Max_Single() * self.L()) / (self.L() + self.L_05())

    def L(self):
        return self.L_0 * (1 - (self.K * math.exp(-self.K * self.LAI)) / (1 - self.m))

    def L_05(self):
        return 2 * self.P_MLT * self.L() - self.L()

    def P_Max_Single(self):
        return self.k() * self.f()

    def k(self):
        return self.LAI * self.k_T_opt * math.exp(-self.H_a * (self.T_opt - self.T_0) / (self.R * self.T_opt * self.T_0))

    def f(self):
        return (1 + math.exp((-self.H_d ** 2 + self.T_opt * self.S) / (self.R * self.H_d * self.T_opt))) / (1 + math.exp((-self.H_d ** 2 + self.T_0 * self.S) / (self.R * self.H_d * self.T_0)))

    
#############################################################################################

    def __call__(self, setPoint: ModelSetPoint, state: ModelState):
        self.setPoint = setPoint
        self.state = state

        return ModelState(self.d_CO2_Air(), self.d_CO2_Top(), self.VP_Air(), self.VP_Top(), self.T())

###USE WHEN TESTING METHODS###
# if __name__ == "__main__": 
#     model = CO2_Model(0,0)
#     model.MC_AirTop(1,1,1,1,1,1,1)