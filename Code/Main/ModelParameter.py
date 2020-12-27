class ModelParameter:
    def __init__(self,
                A_Flr = None, h_Air = None, h_Gh = None, 
                P_Blow = None, phi_ExtCO2 = None, phi_Pad = None, T_Can = None,
                p_Air = None, p_Top = None, K_ThScr = None, eta_ShScrC_d = None, eta_ShScrC_w = None, C_Gh_d = None, C_Gh_w = None, v_Wind = None, h_SideRoof = None,
                A_Roof = None, A_Side = None, c_leakage = None, h_Vent = None, sigma_InsScr = None,
                Res = None, P_MLT = None, L_0 = None, K = None, T_opt = None, k_T_opt = None, LAI = None, H_d = None, S = None,
                c_HECin = None, A_Cov = None, COP_MechCool = None, P_MechCool = None):

        self.h_Air = h_Air # 4.0 | 3.8 | 4.7 | 5.9
        self.h_Gh = h_Gh # 4.8 | 4.2 | 5.1 | 6.1

        self.P_Blow = P_Blow # x | x | x | x
        self.phi_ExtCO2 = phi_ExtCO2 # x | 7.2e4 | 4.3e5 | x
        self.phi_Pad = phi_Pad # x | x | x | 16.7

        self.T_Can = T_Can

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
        self.c_leakage = c_leakage # 1e-4 | 1e-4 | 1e-4 | 1e-4
        self.h_Vent = h_Vent # 1.6 | 0.68 | 0.97 | x
        self.sigma_InsScr = sigma_InsScr # 0.33 | 1 | 1 | x

        self.phi_VentForced = 0 # x | x | x | 0

        self.Res = Res
        self.P_MLT = P_MLT
        self.L_0 = L_0
        self.K = K
        self.T_opt = T_opt
        self.k_T_opt = k_T_opt
        self.H_d = H_d
        self.S = S
        # self.H_a = H_a
        self.LAI = LAI
        self.c_HECin = c_HECin # 2.21 | 1.86 | 1.86 | 2.21
        self.A_Cov = A_Cov
        self.COP_MechCool = COP_MechCool # x | x | x | x 
        self.P_MechCool = P_MechCool # x | x | x | x