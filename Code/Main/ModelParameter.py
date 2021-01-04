class ModelParameter:
    def __init__(self,
        A_Cov=0, A_Flr=0, h_Air=0, h_Elevation=0, h_Gh=0, c_HECin=0,
        A_Roof=0, A_Side=0, h_SideRoof=0, h_Vent=0, C_Gh_d=0, C_Gh_w=0, eta_ShScrC_d=0, eta_ShScrC_w=0, sigma_InsScr=0, c_leakage=0,
        K_ThScr=0,
        eta_Pad=0, phi_Fog=0, phi_Pad=0, phi_VentForced=0, phi_ExtCO2=0, COP_MechCool=0, P_Blow=0, P_MechCool=0,
    ):
        # Construction
        self.A_Cov = A_Cov # 1.7e4 | 1.8e4 | 9.0e4 | 730
        self.A_Flr = A_Flr # 1.3e4 | 1.4e4 | 7.8e4 | 278
        self.h_Air = h_Air # 4.0 | 3.8 | 4.7 | 5.9
        self.h_Elevation = h_Elevation # 104 | 0 | 1470 | 715
        self.h_Gh = h_Gh # 4.8 | 4.2 | 5.1 | 6.1
        self.c_HECin = c_HECin # 2.21 | 1.86 | 1.86 | 2.21

        # Ventilation
        self.A_Roof = A_Roof # 0.2 * 1.3e4 | 0.1 * 1.4e4 | 0.18 * 7.8e4 | x
        self.A_Side = A_Side # 0 | 0 | 0 | x
        self.h_SideRoof = h_SideRoof # x | x | x | x
        self.h_Vent = h_Vent # 1.6 | 0.68 | 0.97 | x
        self.C_Gh_d = C_Gh_d # 0.75 | 0.75 | 0.65 | x
        self.C_Gh_w = C_Gh_w # 0.12 | 0.12 | 0.09 | x
        self.eta_ShScrC_d = eta_ShScrC_d # x | x | x | x
        self.eta_ShScrC_w = eta_ShScrC_w # x | x | x | x
        self.sigma_InsScr = sigma_InsScr # 0.33 | 1 | 1 | x
        self.c_leakage = c_leakage # 1e-4 | 1e-4 | 1e-4 | 1e-4

        # Thermal screen
        self.K_ThScr = K_ThScr # x | 0.05e-3 | 0.25e-3 | 1e-3

        # Active climate control
        self.eta_Pad = eta_Pad  # x | x | x | x
        self.phi_Fog = phi_Fog # x | x | x | 0
        self.phi_Pad = phi_Pad # x | x | x | 16.7
        self.phi_VentForced = phi_VentForced # x | x | x | 0
        self.phi_ExtCO2 = phi_ExtCO2 # x | 7.2e4 | 4.3e5 | x
        self.COP_MechCool = COP_MechCool # x | x | x | x 
        self.P_Blow = P_Blow # x | x | x | x
        self.P_MechCool = P_MechCool # x | x | x | x
