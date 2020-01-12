import numpy as np
from scipy.integrate import odeint
import cantera as ct

RR = 8.314
Patm = 101.3E+3
Patmpsi = Patm * 0.000145038


def psi(P_):
    return (P_ * Patmpsi - Patmpsi)


class Inputs():
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def info(self):
        [print(f" {k}  \t \t  {v}") for k, v in self.__dict__.items()]


class Explosion():
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            for kk, vv in v.__dict__.items():
                setattr(self, kk, vv)

    def info(self, should_print=True):
        items = self.__dict__.items()
        if should_print:
            [print(f" {k}  \t \t  {v}") for k, v in items]
        else:
            return items

    def run(self):
        # Gas Mixtures
        air_species = self.air  # Air
        fuel_species = self.fuel
        phi = self.phi  # Composition
        f = self.f

        # Temperatures and Pressures
        Patm = self.P  # Initial Pressure
        T = self.T  # Initial unburned gas temperature K
        P1 = Patm  # Initial Pressure
        Pa = Patm  # Exit pressure outside vent
        # Tu = T  # Unburned gas temperature
        T1 = T  # Initial Temperature

        # Geometry and Vent
        R = self.R  # Radius
        Cd = self.Cd  # Coefficient for vent
        Av = self.Av  # Vent Area (m2)

        S = self.S

        # Solution Control
        tmax = self.tmax  # Max Time for analysis

        # Create Gases
        carbon = ct.Solution('graphite.xml')
        # Calls Gas Properties from Gri-MECH
        gas_b = ct.Solution('gri30.xml', 'gri30_mix')
        # Calls Gas Properties from Gri-MECH
        gas_bv = ct.Solution('gri30.xml', 'gri30_mix')
        # Calls Gas Properties from Gri-MECH
        gas_u = ct.Solution('gri30.xml', 'gri30_mix')
        mix_phases_b = [(gas_b, 1.0), (carbon, 0.0)]  # Burned Mixture
        mix_phases_u = [(gas_u, 1.0), (carbon, 0.0)]  # Unburned Mixture

        gas_b.set_equivalence_ratio(phi, fuel_species, air_species)
        gas_bv.set_equivalence_ratio(phi, fuel_species, air_species)
        gas_u.set_equivalence_ratio(phi, fuel_species, air_species)
        gas_b.TP = T, Patm
        gas_bv.TP = T, Patm
        gas_u.TP = T, Patm

        unburned = ct.Mixture(mix_phases_u)  # noqa
        burned = ct.Mixture(mix_phases_b)

        # # Calculate Laminar Flamespeed
        # CalcFlamespeed = False
        # if CalcFlamespeed:
        #     # A freely-propagating flat flame
        #     f = ct.FreeFlame(unburned, width=5)
        #     # Energy equation enabled
        #     f.energy_enabled = True
        #     f.set_max_time_step(1000)
        #     f.set_refine_criteria(ratio = 2.0, slope = 0.05, curve = 0.05)
        #     # Solve with multi or mix component transport properties
        #     f.transport_model = 'Mix'
        #     f.solve(loglevel=1,auto=True,refine_grid=True)
        #     S = f.u[0]
        # else:
        #     Xh2 = float(gas_u['H2'].X)
        #     #Laminar Burning Velocity for Hydrogen
        #     # From Liu and MacFarlane for Xh2 < 0.42
        #     A1 = 4.644E-4
        #     A2 = -2.119E-3
        #     A3 = 2.344E-3
        #     A4 = 1.571
        #     A5 = 3.839E-1
        #     A6 = -2.21
        #     xh2O = 0.0  # mol fraction of steam
        #     S = (((A1 + A2*(0.42-Xh2)+A3*(0.42-Xh2)**2) *
        #          Tu**(A4+A5*(0.42-Xh2)))*np.exp(A6*xh2O))

        # Unburned Gas Properties
        cp_aveu = gas_u.cp
        cv_aveu = gas_u.cv
        W_aveu = gas_u.mean_molecular_weight
        rou = gas_u.density

        # Burned Gas Properties
        # Chemical Equilibrium
        # equilibrate the mixture adiabatically at constant P
        burned.equilibrate('HP', solver='gibbs', max_steps=1000)
        cp_aveb = gas_b.cp  # Average Cp
        cv_aveb = gas_b.cv  # Average Cv
        W_aveb = gas_b.mean_molecular_weight  # Average Molecular wt
        rob = gas_b.density  # Average density
        Tb = burned.T
        gas_bv.equilibrate('UV')
        Pf_ = gas_bv.P / Patm

        # Ratio of specific heats for unburned gas = Cp/Cvs
        gammaU = cp_aveu / cv_aveu
        # Ratio of specific heats
        gammaB = cp_aveb / cv_aveb
        gammaE = (gammaU - 1) / (gammaB - 1)
        # gammaE=1.0

        # Initial Volume and Mass
        V1 = 4.0 / 3.0 * np.pi * R ** 3  # Initial Volume
        mi = rou * V1  # Initial Mass

        # print("Unburned Mol Fraction")
        # print(gas_u.species_names,'\n', gas_u.X , '\n',
        #       'Mass Fraction \n', gas_u.Y)
        # print("Burned Mol Fraction")
        # print(gas_b.species_names, '\n',gas_b.X ,'\n',
        #       'Mass Fraction \n', gas_b.Y)
        # print("S:  ",S)
        # print("Tb: ",Tb)
        # print("Pf: ",Pf_)
        # print("GammaE:", gammaE)
        # print("cp_aveb",cp_aveb)

        # start
        # initial conditions
        P_init = 1
        n3init = 1E-5 * (W_aveu / W_aveb) * (Tb / T1)
        ninit = 1E-5
        init = [P_init, n3init, ninit]
        t = np.linspace(0, tmax, 10000)

        # Solve ODE's
        x = odeint(vent_gas_explosion, init, t,
                   args=(P1, R, V1, gammaE, Pf_, gammaU, mi, gas_u, S, rou,
                         rob, gammaB, Cd, Av, f, T1, Pa))

        # Output
        self.P_ = x[:, 0]  # Pressure/initial pressure
        self.n3 = x[:, 1]  # Burnt gas volume
        self.n = x[:, 2]  # Ratio of burnt mass/initial mass
        self.r = R * (self.n3) ** (1.0 / 3.0)  # Spherical flame radius
        self.t = t
        self.nu = 1 - self.n  # Ratio of unburned mass/initial mass
        self.mu = mi * self.nu  # Mass of unburned gas
        # Number of unburned moles
        nmu = self.mu / (gas_u.mean_molecular_weight / 1000)

        self.Vu = (1 - self.n3) * V1
        self.Tu = self.P_ * Patm * self.Vu / (nmu * RR)
        self.gas_u = gas_u
        self.gas_b = gas_b
        self.gas_bv = gas_bv
        self.Tb = Tb
        self.Pf_ = Pf_


def vent_gas_explosion(Y, t, P1, R, V1, gammaE, Pf_, gammaU, mi, gas_u, S, rou,
                       rob, gammaB, Cd, Av, f, T1, Pa):
    P_ = Y[0]
    n3 = Y[1]
    n = Y[2]
    P = P_ * P1

    r = R * (n3) ** (1.0 / 3.0)
    AV1 = 4 * np.pi * r ** 2 / V1
    b = gammaE * Pf_ - 1

    A11 = (1 - n3) * P_ ** (1 / gammaU - 1) / gammaU
    A12 = -P_ ** (1 / gammaU)
    A21 = 1 + n3 ** (gammaE - 1)
    A22 = P_ * (gammaE - 1)

    # St = S * f * P_ ** 0.1
    # nu = 1 - n  # Ratio of unburned mass/initial mass
    # mu = mi * nu  # Mass of unburned gas
    # Number of unburned moles
    # nmu = mu / (gas_u.mean_molecular_weight / 1000)

    # Vu = (1 - n3) * V1
    # Tu = P_ * P1 * Vu / (nmu * RR)
    # St = S * f * (P_ ** 0.1) * ((Tu / T1) ** 1.721)
    St = S * f

    if r < R:  # Unburnt gas venting
        PcriticalInv = (2 / (gammaU + 1)) ** (gammaU / (gammaU - 1))
        if Pa / P < PcriticalInv:
            ddt_mv_mi = Cd * Av * rou / mi * (
                        gammaU * P / rou * ((1 + gammaU) / 2) ** ((1 + gammaU) / (1 - gammaU))) ** 0.5  # noqa
        else:
            ddt_mv_mi = Cd * Av / mi * (2 * gammaU * P * rou / (gammaU - 1) * (P / Pa) ** (2 / gammaU) * (  # noqa
                        1 - (Pa / P) ** ((gammaU - 1) / gammaU))) ** 0.5
        dndt = (AV1) * P_ ** (1 / gammaU) * St
        if n3 >= 1:
            dndt = 0
        B2 = b * dndt - P_ ** (1 - 1 / gammaU) * ddt_mv_mi

    else:  # burnt gas venting
        PcriticalInv = (2 / (gammaB + 1)) ** (gammaB / (gammaB - 1))
        if Pa / P < PcriticalInv:
            ddt_mv_mi = Cd * Av * rob / mi * (
                        gammaB * P / rob * ((1 + gammaB) / 2) ** ((1 + gammaB) / (1 - gammaB))) ** 0.5  # noqa
        else:
            ddt_mv_mi = Cd * Av / mi * (2 * gammaU * P * rob / (gammaB - 1) * (P / Pa) ** (2 / gammaB) * (  # noqa
                        1 - (Pa / P) ** ((gammaB - 1) / gammaB))) ** 0.5
        dndt = (AV1) * P_ ** (1 / gammaU) * St - ddt_mv_mi
        if n3 >= 1:
            dndt = 0
        B2 = b * dndt + (b - gammaE * P_ * n3 / n) * ddt_mv_mi
    B1 = -dndt - ddt_mv_mi
    dPdt = (B1 * A22 - B2 * A12) / (A11 * A22 - A12 * A21)
    dn3dt = (B2 * A11 - B1 * A21) / (A11 * A22 - A12 * A21)
    dydt = [dPdt, dn3dt, dndt]
    return dydt
