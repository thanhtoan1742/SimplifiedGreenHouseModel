class ModelParameter:
    def __init__(self, A_Flr, h_Air, h_Gh, 
                P_Blow, phi_ExtCO2, phi_Pad, CO2_Out, C_Buf, T_Can,
                p_Air, p_Top, K_ThScr, eta_ShScrC_d, eta_ShScrC_w, C_Gh_d, C_Gh_w, v_Wind, h_SideRoof,
                A_Roof, A_Side, T_Out, c_leakage, h_Vent, sigma_InsScr,
                Res, P_MLT, L_0, K, T_opt, k_T_opt):
        self.h_Air = h_Air
        self.h_Gh = h_Gh

        #MC_AirBlow
        self.P_Blow = P_Blow

        #MC_ExtAir
        self.phi_ExtCO2 = phi_ExtCO2

        #MC_PadAir
        self.phi_Pad = phi_Pad
        self.CO2_Out = CO2_Out

        #MC_AirCan
        self.C_Buf = C_Buf
        self.T_Can = T_Can

        #BACH
        self.p_Air = p_Air
        self.p_Top = p_Top
        self.K_ThScr = K_ThScr # x | 0.05e-3 | 0.25e-3 | 1e-3
        self.eta_ShScrC_d = eta_ShScrC_d # x | x | x | x
        self.eta_ShScrC_w = eta_ShScrC_w # x | x | x | x
        self.C_Gh_d = C_Gh_d # 0.75 | 0.75 | 0.65 | x
        self.C_Gh_w = C_Gh_w # 0.12 | 0.12 | 0.09 | x
        self.v_Wind = v_Wind
        self.h_SideRoof = h_SideRoof # x | x | x | x
        self.A_Flr = A_Flr # 1.3e4 | 1.4e4 | 7.8e4 | 278
        self.A_Roof = A_Roof #
        self.A_Side = A_Side #
        self.T_Out = T_Out
        self.c_leakage = c_leakage # 1e-4 | 1e-4 | 1e-4 | 1e-4
        self.h_Vent = h_Vent # 1.6 | 0.68 | 0.97 | x
        self.sigma_InsScr = sigma_InsScr # 0.33 | 1 | 1 | x

        #NGUYEN
        self.phi_VentForced = 0 # x | x | x | 0

        #P
        self.Res = Res
        self.P_MLT = P_MLT
        self.L_0 = L_0
        self.K = K
        self.T_opt = T_opt
        self.k_T_opt = k_T_opt

