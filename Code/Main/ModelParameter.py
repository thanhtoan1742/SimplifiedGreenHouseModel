class ModelParameter:
    def __init__(self,
                A_Flr = None, h_Air = None, h_Gh = None, P_Blow = None, phi_ExtCO2 = None, 
                phi_Pad = None, K_ThScr = None, eta_ShScrC_d = None, 
                eta_ShScrC_w = None, C_Gh_d = None, C_Gh_w = None, h_SideRoof = None,
                A_Roof = None, A_Side = None, c_leakage = None, h_Vent = None, sigma_InsScr = None,
                P_MLT = None, L_0 = None, K = None, k_T_opt = None, LAI = None, 
                S = None, c_HECin = None, A_Cov = None, COP_MechCool = None, P_MechCool = None, 
                eta_Pad = None, phi_Fog = None, 
                h_Elevation = None):

        self.h_Air = h_Air # 4.0 | 3.8 | 4.7 | 5.9
        self.h_Gh = h_Gh # 4.8 | 4.2 | 5.1 | 6.1
        self.h_Vent = h_Vent # 1.6 | 0.68 | 0.97 | x
        self.h_SideRoof = h_SideRoof # x | x | x | x

        self.A_Flr = A_Flr # 1.3e4 | 1.4e4 | 7.8e4 | 278
        self.A_Roof = A_Roof # 0.2 * 1.3e4 | 0.1 * 1.4e4 | 0.18 * 7.8e4 | x
        self.A_Side = A_Side # 0 | 0 | 0 | x
        self.A_Cov = A_Cov

        self.C_Gh_d = C_Gh_d # 0.75 | 0.75 | 0.65 | x
        self.C_Gh_w = C_Gh_w # 0.12 | 0.12 | 0.09 | x

        self.P_Blow = P_Blow # x | x | x | x
        self.phi_ExtCO2 = phi_ExtCO2 # x | 7.2e4 | 4.3e5 | x
        self.phi_Pad = phi_Pad # x | x | x | 16.7

        self.K_ThScr = K_ThScr # x | 0.05e-3 | 0.25e-3 | 1e-3
        self.eta_ShScrC_d = eta_ShScrC_d # x | x | x | x
        self.eta_ShScrC_w = eta_ShScrC_w # x | x | x | x
        self.c_leakage = c_leakage # 1e-4 | 1e-4 | 1e-4 | 1e-4
        self.sigma_InsScr = sigma_InsScr # 0.33 | 1 | 1 | x

        self.phi_VentForced = 0 # x | x | x | 0

        self.P_MLT = P_MLT
        self.L_0 = L_0
        self.K = K
        self.k_T_opt = k_T_opt
        self.S = S
        self.LAI = LAI # Vanthoor page 31
        self.c_HECin = c_HECin # 2.21 | 1.86 | 1.86 | 2.21
        self.COP_MechCool = COP_MechCool # x | x | x | x 
        self.P_MechCool = P_MechCool # x | x | x | x
        self.eta_Pad = eta_Pad  # x | x | x | x

        self.phi_Fog = phi_Fog # x | x | x | 0

        self.h_Elevation = h_Elevation # 104 | 0 | 1470 | 715