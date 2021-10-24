# import xlwings as xw
import numpy as np
from CoolProp import CoolProp as cp
from scipy import constants as constant
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import integrate
from scipy import optimize
import warnings
import plotly.express as px
import plotly.graph_objects as go
from scipy.interpolate import griddata

#===========================PLOTLY VERSION OF THE CODE===================================================
#========================================================================================================

class Fluid:
    def __init__(self, temperature, pressure, species, diameter=None, velocity=None, mass_fraction=None):

        self.temperature = temperature
        self.pressure = pressure
        self.species = species
        self.velocity = velocity
        self.diameter = diameter
        self.density = cp.PropsSI(['D'], 'P', self.pressure, 'T', self.temperature, species)
        self.molecular_weight = cp.PropsSI(species, 'molemass')
        self.specific_heat = cp.PropsSI(['C'], 'P', self.pressure, 'T', self.temperature, self.species)
        self.mass_fraction = mass_fraction

    def update(self, temperature=None, pressure=None, velocity=None, density=None, diameter=None, mass_flow_rate=None,
               mass_fraction=None, choked=None):

        if choked is not None:
            self.choked = choked

        if temperature is not None and pressure is not None:
            self.temperature = temperature
            self.pressure = pressure
            self.density = cp.PropsSI(['D'], 'P', self.pressure, 'T', float(self.temperature), self.species)

        elif temperature is not None and density is not None:
            self.temperature = temperature
            self.density = density
            self.pressure = cp.PropsSI(['P'], 'D', float(self.density), 'T', float(self.temperature), self.species)

        elif pressure != None and density != None:
            self.density = density
            self.pressure = pressure
            self.temperature = cp.PropsSI(['T'], 'D', float(self.density), 'P', float(self.pressure), self.species)

        if diameter is not None and velocity is not None:
            self.diameter = diameter
            self.velocity = velocity
            self.mass_flow_rate = self.density * np.pi * self.diameter ** 2 / 4 * self.velocity

        elif mass_flow_rate is not None and velocity is not None:
            self.mass_flow_rate = mass_flow_rate
            self.velocity = velocity
            self.diameter = np.sqrt(4 * self.mass_flow_rate / (self.density * self.velocity * np.pi))

        if mass_fraction is not None:
            self.mass_fraction = mass_fraction


class JetModel:
    def __init__(self, ambient_temperature, ambient_pressure, release_temperature, release_pressure, orifice_diameter,
                 release_angle, min_concentration, point_along_pathline,
                 contour_of_interest, velocity_if_not_sonic=None):
        self.release_angle = release_angle
        self.orifice_diameter = orifice_diameter
        self.velocity_if_not_sonic = velocity_if_not_sonic
        self.min_concentration = min_concentration if min_concentration is not None else 7e-4
        self.contour_of_interest = contour_of_interest if contour_of_interest is not None else 0.04
        self.point_along_pathline = point_along_pathline
        self.lam = 1.16
        self.point_along_pathline = point_along_pathline if point_along_pathline is not None else 0

        self.H2_fluid = Fluid(release_temperature, release_pressure, 'H2', diameter=orifice_diameter,
                              velocity=self.velocity_if_not_sonic, mass_fraction=1)
        self.ambient_fluid = Fluid(ambient_temperature, ambient_pressure, 'AIR')

    def run(self):
        self._point_1()
        self._point_2()
        #self._point_3()
        self._point_4()
        self._integration_zone()
        self._format_solution()
        self._separation_distance()

    def generate_all_plots(self):
        return self.centerline_velocity_plot(), self.centerline_mass_concentration_plot(), self.centerline_mole_concentration_plot(), self.theta_plot(), self.concentration_profile_plot(), self.contour_plot_1(), self.contour_plot_2()

    def _point_1(self):

        # enthalpy and entropy at source
        self.enthalpy_at_0 = cp.PropsSI(['H'], 'P', self.H2_fluid.pressure, 'T', self.H2_fluid.temperature, 'H2')
        self.entropy_at_0 = cp.PropsSI(['S'], 'P', self.H2_fluid.pressure, 'T', self.H2_fluid.temperature, 'H2')

        # Function for finding pressure at 1 if flow is choked
        def error_velocity(pressure):
            try:
                speed_of_sound = cp.PropsSI(['A'], 'P', pressure, 'S', float(self.entropy_at_0), 'H2')
            except:
                speed_of_sound = 1000
            enthalpy = cp.PropsSI(['H'], 'P', pressure, 'S', float(self.entropy_at_0), 'H2')
            if self.enthalpy_at_0 - enthalpy > 0:
                velocity_from_energy_conservation = np.sqrt(2 * (self.enthalpy_at_0 - enthalpy))
            else:
                velocity_from_energy_conservation = 0
            return velocity_from_energy_conservation - speed_of_sound
        
      

        # Find if flow is choked   
        if self.H2_fluid.pressure > 1.9 * self.ambient_fluid.pressure:
            if self.velocity_if_not_sonic is not None:
                warnings.warn("Flow over specified, release velocity not used")

            pressure_at_1 = optimize.brentq(error_velocity, self.H2_fluid.pressure, self.ambient_fluid.pressure)
            self.pressure_at_1 = pressure_at_1
            temperature_at_1 = cp.PropsSI(['T'], 'P', pressure_at_1, 'S', float(self.entropy_at_0), 'H2')
            velocity_at_1 = cp.PropsSI(['A'], 'P', pressure_at_1, 'S', float(self.entropy_at_0), 'H2')
            # Update fluid object with properties at 1
            self.H2_fluid.update(temperature=temperature_at_1, pressure=pressure_at_1, velocity=velocity_at_1,
                                 diameter=self.orifice_diameter, choked=True)

        else:
            self.choked = False
            if self.velocity_if_not_sonic is None:
                warnings.warn("Velocity required if flow is subsonic")
            temperature_at_1 = cp.PropsSI(['T'], 'P', self.ambient_fluid.pressure, 'S', float(self.entropy_at_0), 'H2')
            # Update fluid object with properties at 1
            self.H2_fluid.update(pressure=self.ambient_fluid.pressure, temperature=temperature_at_1,
                                 velocity=self.velocity_if_not_sonic, choked=False)

    def _point_2(self):
        # Only is choked, if not choked properties stay the same
        if self.H2_fluid.choked:
            # from notional nozzle model
            velocity_at_2 = (self.H2_fluid.diameter ** 2 / 4 * np.pi * (
                    self.H2_fluid.pressure - self.ambient_fluid.pressure) + self.H2_fluid.mass_flow_rate * self.H2_fluid.velocity) / self.H2_fluid.mass_flow_rate
            enthalpy_at_1 = cp.PropsSI(['H'], 'P', float(self.H2_fluid.pressure), 'T', float(self.H2_fluid.temperature),
                                       'H2')
            enthalpy_at_2 = enthalpy_at_1 + 1 / 2 * self.H2_fluid.velocity ** 2 - 1 / 2 * velocity_at_2 ** 2
            temperature_at_2 = cp.PropsSI(['T'], 'P', self.ambient_fluid.pressure, 'H', enthalpy_at_2, 'H2')
            self.H2_fluid.update(pressure=self.ambient_fluid.pressure, temperature=temperature_at_2,
                                 velocity=velocity_at_2, mass_flow_rate=self.H2_fluid.mass_flow_rate)

    def _point_3(self):

        arbitrary_temperature = 47

        def error_energy_equation(mass_air):
            mass_at_3 = self.H2_fluid.mass_flow_rate + mass_air
            mass_fraction_H2_at_3 = self.H2_fluid.mass_flow_rate / mass_at_3
            enthalpy_H2 = cp.PropsSI(['H'], 'P', float(self.H2_fluid.pressure), 'T', float(arbitrary_temperature), 'H2')
            enthalpy_air = cp.PropsSI(['H'], 'P', float(self.ambient_fluid.pressure), 'T',
                                      float(self.ambient_fluid.temperature), 'AIR')
            enthalpy_mixture = mass_fraction_H2_at_3 * enthalpy_H2 + (1 - mass_fraction_H2_at_3) * enthalpy_air
            velocity_at_3 = self.H2_fluid.mass_flow_rate * self.H2_fluid.velocity / mass_at_3
            residual = self.H2_fluid.mass_flow_rate * (
                    enthalpy_at_2 + 0.5 * self.H2_fluid.velocity ** 2) - mass_at_3 * (
                               enthalpy_mixture + 0.5 * velocity_at_3 ** 2)
            return residual, mass_at_3, velocity_at_3, mass_fraction_H2_at_3

        if self.H2_fluid.temperature < arbitrary_temperature:
            enthalpy_at_1 = cp.PropsSI(['H'], 'P', float(self.H2_fluid.pressure), 'T', float(self.H2_fluid.temperature),
                                       'H2')
            enthalpy_at_2 = enthalpy_at_1 + 1 / 2 * self.H2_fluid.velocity ** 2 - 1 / 2 * self.H2_fluid.velocity ** 2
            mass_air_entrained = optimize.brentq(lambda x: error_energy_equation(x)[0], -100, 100)
            mass_at_3 = error_energy_equation(mass_air_entrained)[1]
            velocity_at_3 = error_energy_equation(mass_air_entrained)[2]
            mass_fraction_H2_at_3 = error_energy_equation(mass_air_entrained)[3]
            # Update fluid object
            self.H2_fluid.update(temperature=arbitrary_temperature, velocity=velocity_at_3,
                                 pressure=self.ambient_fluid.pressure, mass_flow_rate=mass_at_3,
                                 mass_fraction=mass_fraction_H2_at_3)

    def _point_4(self):
        BE = self.H2_fluid.diameter / np.sqrt(
            2 * (2 * self.lam ** 2 + 1) / (
                    self.lam ** 2 * self.H2_fluid.density / self.ambient_fluid.density + self.lam ** 2 + 1))
        v_cl = self.H2_fluid.velocity
        Y_cl = self.H2_fluid.mass_fraction * (self.lam ** 2 + 1.) / (2. * self.lam ** 2)
        enthalpy_ambient = cp.PropsSI(['H'], 'P', self.ambient_fluid.pressure, 'T', self.ambient_fluid.temperature,
                                      'AIR')
        Cp_gas = cp.PropsSI(['C'], 'P', self.ambient_fluid.pressure, 'T',
                            (self.H2_fluid.temperature + self.ambient_fluid.temperature) / 2, 'H2')
        MW_cl = 1.0 / (Y_cl / self.H2_fluid.molecular_weight + (1.0 - Y_cl) / self.ambient_fluid.molecular_weight)
        Cp_mix = self.H2_fluid.mass_fraction * Cp_gas + (
                1.0 - self.H2_fluid.mass_fraction) * self.ambient_fluid.specific_heat
        enthalpy_mixture = Cp_mix * self.H2_fluid.temperature
        enthalpy_cl = enthalpy_ambient + (self.lam ** 2 + 1.) / (2. * self.lam ** 2) * (
                enthalpy_mixture - enthalpy_ambient)
        Cp_cl = Y_cl * Cp_gas + (1.0 - Y_cl) * self.ambient_fluid.specific_heat
        T_cl = enthalpy_cl / Cp_cl
        rho_cl = self.ambient_fluid.pressure * MW_cl / (constant.R * T_cl)
        distance_along_s = 6.2 * self.H2_fluid.diameter
        x, y, S = 0, 0, 0
        initial_x = x + distance_along_s * np.cos(self.release_angle)
        initial_y = y + distance_along_s * np.sin(self.release_angle)
        self.initial_S = S + distance_along_s
        self.conditions = [v_cl, BE, rho_cl, Y_cl, self.release_angle, initial_x, initial_y]

    def _integration_zone(self, max_steps=100000, Smax=np.inf):
        dS = 500 * self.orifice_diameter
        r = integrate.ode(self._gov_equations)
        r.set_integrator('dopri5', atol=1e-6, rtol=1e-6)
        T, Y = [], []

        def solout(t, y):
            T.append(t)
            Y.append(np.array(y))

        r.set_solout(solout)
        r.set_initial_value(self.conditions, self.initial_S)
        i = 0
        while r.successful() and r.y[3] > self.min_concentration and i < max_steps and r.t < Smax:
            r.integrate(r.t + dS)
            i += 1

        self.Y = np.array(Y)
        self.T = np.array(T)

    def _format_solution(self):
        MW = self.ambient_fluid.molecular_weight * self.H2_fluid.molecular_weight / (self.Y[:, 3] * (
                self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) + self.H2_fluid.molecular_weight)
        mole_fraction = self.Y[:, 3] * MW / self.H2_fluid.molecular_weight
        solution = np.append(self.Y, mole_fraction.reshape(mole_fraction.shape[0], 1), axis=1)

        self.__solution__ = {}

        for key, val in zip(['V_cl', 'B', 'rho_cl', 'Y_cl', 'theta', 'x', 'y', 'mole_fraction'], solution.T):
            self.__solution__[key] = val
        self.__solution__['S'] = self.T

    def _calculate_entrainment(self, V_cl, B, rho_cl, theta, alpha):
        FrL = V_cl ** 2 * rho_cl / (constant.g * B * abs(self.ambient_fluid.density - rho_cl))
        Fr = self.H2_fluid.velocity / np.sqrt(constant.g * self.H2_fluid.diameter * abs(
            self.ambient_fluid.density - self.H2_fluid.density) / self.H2_fluid.density)
        if Fr < 268:
            alpha_buoy = 17.313 - 0.11665 * Fr + 2.0771e-4 * Fr ** 2
        else:
            alpha_buoy = 0.97

        E_buoy = alpha_buoy / FrL * (2 * constant.pi * V_cl * B) * np.sin(theta)
        BetaA = .28

        Emom = BetaA * np.sqrt(constant.pi / 4.0 * self.H2_fluid.diameter ** 2 *
                               self.H2_fluid.density * self.H2_fluid.velocity ** 2 / self.ambient_fluid.density)

        E = Emom + E_buoy
        alphatest = E / (2 * constant.pi * V_cl * B)
        if alphatest > alpha:
            E = alpha * 2 * constant.pi * B * V_cl
        return E

    def _continuity_equation(self, rho_cl, B, V_cl, E):
        LHScont = np.array([(self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B ** 2,  # d/dS(V_cl)
                            2 * (self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B * V_cl,  # d/dS(B)
                            self.lam ** 2 * B ** 2 * V_cl,  # d/dS(rho_cl)
                            0.,  # d/dS(Y_cl)

                            0.]) * constant.pi / (self.lam ** 2 + 1)  # d/dS(theta)
        RHScont = self.ambient_fluid.density * E
        return LHScont, RHScont

    def _x_momentum_equation(self, rho_cl, V_cl, theta, B):
        LHSxmom = np.array(
            [(2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B ** 2 * V_cl * np.cos(theta),  # d/dS(V_cl)
             (2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B * V_cl ** 2 * np.cos(theta),  # d/dS(B)
             self.lam ** 2 * B ** 2 * V_cl ** 2 * np.cos(theta),  # d/dS(rho_cl)
             0.,  # d/dS(Y_cl)
             -(2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * (B * V_cl) ** 2 * np.sin(theta) / 2
             # d/dS(theta)
             ]) * constant.pi / (2 * self.lam ** 2 + 1)
        RHSxmom = 0.
        return LHSxmom, RHSxmom

    def _y_momentum_equation(self, rho_cl, V_cl, theta, B):
        LHSymom = np.array(
            [(2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B ** 2 * V_cl * np.sin(theta),  # d/dS(V_cl)
             (2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B * V_cl ** 2 * np.sin(theta),  # d/dS(B)
             self.lam ** 2 * B ** 2 * V_cl ** 2 * np.sin(theta),  # d/dS(rho_cl)
             0.,  # d/dS(Y_cl)
             (2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * (B * V_cl) ** 2 * np.cos(theta) / 2
             # d/dS(theta)
             ]) * constant.pi / (2 * self.lam ** 2 + 1)
        RHSymom = -constant.pi * self.lam ** 2 * constant.g * (rho_cl - self.ambient_fluid.density) * B ** 2
        return LHSymom, RHSymom

    def _species_equation(self, rho_cl, Y_cl, B, V_cl):
        LHSspec = np.array([B * Y_cl * rho_cl,  # d/dS(V_cl)
                            2 * V_cl * Y_cl * rho_cl,  # d/dS(B)
                            B * V_cl * Y_cl,  # d/dS(rho_cl)
                            B * V_cl * rho_cl,  # d/dS(Y_cl)
                            0.,  # d/dS(theta)
                            ]) * constant.pi * self.lam ** 2 * B / (self.lam ** 2 + 1)
        RHSspec = 0
        return LHSspec, RHSspec


    def _energy_equation(self, RHScont, rho_cl, V_cl, B, Y_cl, numB=5, numpts=500):
        h_amb = self.ambient_fluid.specific_heat * self.ambient_fluid.temperature
        Cp_fluid = cp.PropsSI(['C'], 'P', float(self.H2_fluid.pressure), 'T', float(self.H2_fluid.temperature), 'H2')
        r = np.append(np.array([0]), np.logspace(-5, np.log10(numB * B), numpts))
        zero = np.zeros_like(r)
        V = V_cl * np.exp(-(r ** 2) / (B ** 2))
        rho = (rho_cl - self.ambient_fluid.density) * np.exp(
            -(r ** 2) / ((self.lam * B) ** 2)) + self.ambient_fluid.density
        Y = Y_cl * rho_cl / rho * np.exp(-r ** 2 / (self.lam * B) ** 2)
        self.MW = self.ambient_fluid.molecular_weight * self.H2_fluid.molecular_weight / (Y * (
                self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) + self.H2_fluid.molecular_weight)
        dYdS = np.array([zero,  # d/dS(V_cl)
                         (2 * Y ** 2 * self.ambient_fluid.density * r ** 2 * np.exp(r ** 2 / (self.lam * B) ** 2) /
                          (self.lam ** 2 * B ** 3 * Y_cl * rho_cl)),  # d/dS(B)
                         Y ** 2 * self.ambient_fluid.density * (np.exp(r ** 2 / (self.lam * B) ** 2) - 1) / (
                                 Y_cl * rho_cl ** 2),
                         # d/dS(rho_cl)
                         Y / Y_cl,  # d/dS(Y_cl)
                         zero])  # d/dS(theta)
        dMWdS = (self.MW * (self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) / (
                self.H2_fluid.molecular_weight * (Y - 1) - self.ambient_fluid.molecular_weight * Y)) * dYdS
        Cp = Y * (Cp_fluid - self.ambient_fluid.specific_heat) + self.ambient_fluid.specific_heat
        dCpdS = (Cp_fluid - self.ambient_fluid.specific_heat) * dYdS
        rhoh = self.ambient_fluid.pressure / constant.R * self.MW * Cp
        drhohdS = self.ambient_fluid.pressure / constant.R * (self.MW * dCpdS + Cp * dMWdS)
        dVdS = np.array([V / V_cl,  # d/dS(V_cl)
                         2 * V * r ** 2 / B ** 3,  # d/dS(B)
                         zero,  # d/dS(rho_cl)
                         zero,  # d/dS(Y_cl)
                         zero])  # d/dS(theta)

        LHSener = 2 * constant.pi * integrate.trapz(V * drhohdS * r + rhoh * dVdS * r, r)
        LHSener += [
            constant.pi / (6 * self.lam ** 2 + 2) * (
                    3 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B ** 2 * V_cl ** 2,
            # d/dS(V_cl)
            constant.pi / (9 * self.lam ** 2 + 3) * (
                    3 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * V_cl ** 3 * B,
            # d/dS(B)
            constant.pi / (6 * self.lam ** 2 + 2) * self.lam ** 2 * B ** 2 * V_cl ** 3,  # d/dS(rho_cl)
            0.,  # d/dS(Y_cl)
            0.]  # d/dS(theta)

        RHSener = h_amb * RHScont
        return LHSener, RHSener

    def _gov_equations(self, S, ind_vars, alpha=0.082):
        [V_cl, B, rho_cl, Y_cl, theta, x, y] = ind_vars
        E = self._calculate_entrainment(V_cl, B, rho_cl, theta, alpha)
        # governing equations:

        LHScont, RHScont = self._continuity_equation(rho_cl, B, V_cl, E)
        LHSxmom, RHSxmom = self._x_momentum_equation(rho_cl, V_cl, theta, B)
        LHSymom, RHSymom = self._y_momentum_equation(rho_cl, V_cl, theta, B)
        LHSspec, RHSspec = self._species_equation(rho_cl, Y_cl, B, V_cl)
        LHSener, RHSener = self._energy_equation(RHScont, rho_cl, V_cl, B, Y_cl, numB=5, numpts=500)

        LHS = np.array([LHScont,
                        LHSxmom,
                        LHSymom,
                        LHSspec,
                        LHSener
                        ])
        RHS = np.array([RHScont,
                        RHSxmom,
                        RHSymom,
                        RHSspec,
                        RHSener])

        dz = np.append(np.linalg.solve(LHS, RHS), np.array([np.cos(theta), np.sin(theta)]), axis=0)
        return dz

    def centerline_velocity_plot(self):
        fig = px.line( x = self.__solution__['S'],
              y = self.__solution__['V_cl'],
              title = 'Centerline velocity along path')

        fig['data'][0]['showlegend']=False
        fig['data'][0]['name'] = 'Velocity'
        fig.update_layout(xaxis_title='S (m)', yaxis_title = 'V_cl (m/s)', font=dict(family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
        # fig.show()
        return fig

    def centerline_mass_concentration_plot(self):
        fig = px.line( x = self.__solution__['S'],
              y = self.__solution__['Y_cl'],
              title = 'Centerline mass concentration along path')

        fig['data'][0]['showlegend']=False
        fig['data'][0]['name'] = 'Mass concentration'
        fig.update_layout(xaxis_title='S (m)', yaxis_title = 'Y_cl (m/s)', font=dict(family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
        # fig.show()
        return fig


    def centerline_mole_concentration_plot(self):

        MW = self.ambient_fluid.molecular_weight * self.H2_fluid.molecular_weight / (self.__solution__['Y_cl'] * (
                self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) + self.H2_fluid.molecular_weight)
        mole_concentration = self.__solution__['Y_cl'] * MW / self.H2_fluid.molecular_weight

        fig = px.line( x = self.__solution__['S'], y = mole_concentration, title = 'Centerline mole concentration along path')

        fig['data'][0]['showlegend']=False
        fig['data'][0]['name'] = 'Mole concentration'
        fig.update_layout(xaxis_title='S (m)', yaxis_title = 'X_cl (m/s)', font=dict(family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
        # fig.show()
        return fig

    def theta_plot(self):
        fig = px.line( x = self.__solution__['S'],
              y = self.__solution__['theta'],
              title = 'Curve angle')
        fig['data'][0]['showlegend']=False
        fig['data'][0]['name'] = 'Theta'
        fig.update_layout(xaxis_title='S (m)', yaxis_title = 'Theta (rad)', font=dict(family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
        # fig.show()
        return fig


    def concentration_profile_plot(self):
        nums = np.linspace(30, len(self.__solution__['S']) - 1, 10)
        nums = np.round(nums).astype(int)
        r = np.linspace(-2 * self.__solution__['B'], 2 * self.__solution__['B'], 100).reshape(100, len(
            self.__solution__['S']))
        V = self.__solution__['V_cl'].T * np.exp(-r ** 2 / self.__solution__['B'] ** 2) / 50
        rho_cl = self.__solution__['rho_cl']
        rho = (rho_cl - self.ambient_fluid.density) * np.exp(
            -r ** 2 / (self.__solution__['B'] ** 2 * self.lam ** 2)) + self.ambient_fluid.density
        Y_concentration = 1 / rho * rho_cl * self.__solution__['Y_cl'] * np.exp(
            -r ** 2 / (self.__solution__['B'] ** 2 * self.lam ** 2))
        R = self.rotation_matrix(self.__solution__['theta'])
        # multiply by 200 so profiles don't look so small
        transformed_coords_cons = np.array([r, Y_concentration * 200]).T @ R.T
    

        x_values = transformed_coords_cons[:, :, 0].T + self.__solution__['x']
        y_values = transformed_coords_cons[:, :, 1].T + self.__solution__['y']
        
        fig = go.Figure()
        
        for num in nums:
            fig.add_trace(go.Scatter(x=x_values[:,num],y=y_values[:,num],fill='toself',  fillcolor='rgba(255, 0, 0, 0.1)',
                    hoveron = 'points+fills', # select where hover is active
                    line_color='red', showlegend=False))
        fig['data'][0]['showlegend']=True
        fig['data'][0]['name'] = 'Qualitative concentration profile'
        
        fig.update_layout(xaxis_title='x (m)', yaxis_title = 'y (m)', font=dict(family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
        # fig.show()
        return fig
        


    def _contour_data(self):
        iS_ = np.arange(len(self.__solution__['S']))
        poshalf = np.logspace(-5, np.log10(3 * np.max(self.__solution__['B'])))
        r_ = np.concatenate((-1.0 * poshalf[::-1], [0], poshalf))
        r, iS = np.meshgrid(r_, iS_)

        B = self.__solution__['B'][iS]
        rho_cl = self.__solution__['rho_cl'][iS]
        Y_cl = self.__solution__['Y_cl'][iS]
        rho = (rho_cl - self.ambient_fluid.density) * np.exp(
            -r ** 2 / (B ** 2 * 1.16 ** 2)) + self.ambient_fluid.density
        Y_concentration = 1 / rho * rho_cl * Y_cl * np.exp(-r ** 2 / (B ** 2 * self.lam ** 2))
        MW = self.ambient_fluid.molecular_weight * self.H2_fluid.molecular_weight / (Y_concentration * (
                self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) + self.H2_fluid.molecular_weight)
        X_concentration = Y_concentration * MW / self.H2_fluid.molecular_weight
        x = self.__solution__['x'][iS] + r * np.sin(self.__solution__['theta'][iS])
        y = self.__solution__['y'][iS] - r * np.cos(self.__solution__['theta'][iS])
        return x, y, X_concentration

    def _separation_distance(self):
        x, y, X_concentration = self._contour_data()
        contour = plt.contour(x, y, X_concentration, levels=[self.contour_of_interest], colors='white', alpha=1,
                              linewidths=4)
        plt.close()
        line = np.array(contour.allsegs)
        line = line[:, 0, :, :].reshape(np.shape(line)[2], 2)

        if self.release_angle <= np.pi / 2 and self.release_angle >= 0:
            x_arg = np.argmax(line[:, 0])
            y_arg = np.argmax(line[:, 1])

        elif self.release_angle > np.pi / 2 and self.release_angle <= np.pi:
            x_arg = np.argmin(line[:, 0])
            y_arg = np.argmax(line[:, 1])

        elif self.release_angle > np.pi and self.release_angle <= 3 / 2 * np.pi:
            x_arg = np.argmin(line[:, 0])
            y_arg = np.argmin(line[:, 1])

        elif self.release_angle > 3 / 2 * np.pi and self.release_angle <= 2 * np.pi:
            x_arg = np.argmax(line[:, 0])
            y_arg = np.argmin(line[:, 1])

        else:
            x_arg = np.argmax(line[:, 0])
            y_arg = np.argmax(line[:, 1])

        self.max_x_coords = line[x_arg, :]
        self.max_y_coords = line[y_arg, :]

    def contour_plot_1(self):
        x, y, X_concentration = self._contour_data()
        positions = np.vstack([x.ravel(), y.ravel()])
        x = positions[0,:]
        y = positions[1,:]
        z = X_concentration.flatten()
        
        xi = np.linspace(x.min(),x.max(),200)
        yi = np.linspace(y.min(),y.max(),200)

        zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
        zi[zi < 0.00001] = 0
        
            
        layout = go.Layout(title = 'Mole concentration contour plot along pathline',xaxis = go.XAxis(title = 'x (m)', showgrid=False),yaxis = go.YAxis(
        title = 'y (m)',showgrid=False
    )
)
        trace = go.Contour(x=xi, y=yi, z = zi, colorscale ='amp', line_smoothing=0.85, contours=dict(
            coloring ='heatmap',
            showlabels = True, # show labels on contours
            labelfont = dict( # label font properties
                size = 12,
                color = 'white',
            )))
        data = [trace]
        fig = go.Figure(data, layout_yaxis_range=[-0.5,0.5], layout=layout)
        fig.update_yaxes(
    scaleanchor = "x",
    scaleratio = 1,
  )
        fig.update_xaxes(range=[1, 1.5])
        fig.update_layout(font=dict(family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
        # fig.show()
        return fig


    def contour_plot_2(self):
        S_idx = np.argmin(np.abs(self.point_along_pathline - self.__solution__['S']))
        x_ = np.linspace(-5, 5, num=1500)
        y_ = np.linspace(-5, 5, num=1500)
        x, y = np.meshgrid(x_, y_)
        B = self.__solution__['B'][S_idx]
        rho_cl = self.__solution__['rho_cl'][S_idx]
        Y_cl = self.__solution__['Y_cl'][S_idx]
        rho = (rho_cl - self.ambient_fluid.density) * np.exp(
            -(x ** 2 + y ** 2) ** 2 / (B ** 2 * self.lam ** 2)) + self.ambient_fluid.density
        Y_concentration = 1 / rho * rho_cl * Y_cl * np.exp(-(x ** 2 + y ** 2) ** 2 / (B ** 2 * self.lam ** 2))
        MW = self.ambient_fluid.molecular_weight * self.H2_fluid.molecular_weight / (Y_concentration * (
                self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) + self.H2_fluid.molecular_weight)
        X_concentration = Y_concentration * MW / self.H2_fluid.molecular_weight
        
        
        layout = go.Layout(title = 'Mole concentration contour plot {} m <br> along pathline, perpendicular to pathline'.format(
            np.round(self.__solution__['S'][S_idx], 3)),xaxis = go.XAxis(title = 'r (m)', showgrid=False),yaxis = go.YAxis(
        title = 'r (m)',showgrid=False
    )
)
        trace = go.Contour(x=x_, y=y_, z = X_concentration, colorscale ='amp', line_smoothing=0.85, contours=dict(
            coloring ='heatmap',
            showlabels = True, # show labels on contours
            labelfont = dict( # label font properties
                size = 12,
                color = 'white',
            )))
        data = [trace]
        fig = go.Figure(data, layout_yaxis_range=[-0.2,0.2], layout=layout)
        fig.update_yaxes(
            scaleanchor = "x",
            scaleratio = 1,)
        fig.update_xaxes(range=[-0.1, 0.1])
        fig.update_yaxes(automargin=True)
        fig.update_layout(font=dict(family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
        
        # fig.show()
        return fig

    def rotation_matrix(self, theta):
        return np.array([[np.cos(theta - np.pi / 2), -np.sin(theta - np.pi / 2)],
                         [np.sin(theta - np.pi / 2), np.cos(theta - np.pi / 2)]])

#============================END PLOTLY VERSION OF THE CODE=======================
#=================================================================================


#============================MATPLOTLIB VERSION OF THE CODE=======================
#=================================================================================
# class Fluid:
#     def __init__(self, temperature, pressure, species, diameter=None, velocity=None, mass_fraction=None):

#         self.temperature = temperature
#         self.pressure = pressure
#         self.species = species
#         self.velocity = velocity
#         self.diameter = diameter
#         self.density = cp.PropsSI(['D'], 'P', self.pressure, 'T', self.temperature, species)
#         self.molecular_weight = cp.PropsSI(species, 'molemass')
#         self.specific_heat = cp.PropsSI(['C'], 'P', self.pressure, 'T', self.temperature, self.species)
#         self.mass_fraction = mass_fraction

#     def update(self, temperature=None, pressure=None, velocity=None, density=None, diameter=None, mass_flow_rate=None,
#                mass_fraction=None, choked=None):

#         if choked is not None:
#             self.choked = choked

#         if temperature is not None and pressure is not None:
#             self.temperature = temperature
#             self.pressure = pressure
#             self.density = cp.PropsSI(['D'], 'P', self.pressure, 'T', float(self.temperature), self.species)

#         elif temperature is not None and density is not None:
#             self.temperature = temperature
#             self.density = density
#             self.pressure = cp.PropsSI(['P'], 'D', float(self.density), 'T', float(self.temperature), self.species)

#         elif pressure != None and density != None:
#             self.density = density
#             self.pressure = pressure
#             self.temperature = cp.PropsSI(['T'], 'D', float(self.density), 'P', float(self.pressure), self.species)

#         if diameter is not None and velocity is not None:
#             self.diameter = diameter
#             self.velocity = velocity
#             self.mass_flow_rate = self.density * np.pi * self.diameter ** 2 / 4 * self.velocity

#         elif mass_flow_rate is not None and velocity is not None:
#             self.mass_flow_rate = mass_flow_rate
#             self.velocity = velocity
#             self.diameter = np.sqrt(4 * self.mass_flow_rate / (self.density * self.velocity * np.pi))

#         if mass_fraction is not None:
#             self.mass_fraction = mass_fraction

# class JetModel:
#     def __init__(self, ambient_temperature, ambient_pressure, release_temperature, release_pressure, orifice_diameter,
#                  release_angle, min_concentration, X_contour_range, Y_contour_range, point_along_pathline,
#                  contour_of_interest, velocity_if_not_sonic=None):
#         self.release_angle = release_angle
#         self.orifice_diameter = orifice_diameter
#         self.velocity_if_not_sonic = velocity_if_not_sonic
#         self.min_concentration = min_concentration if min_concentration is not None else 7e-4
#         self.contour_of_interest = contour_of_interest if contour_of_interest is not None else 0.04
#         self.Y_contour_range = Y_contour_range
#         self.X_contour_range = X_contour_range
#         self.point_along_pathline = point_along_pathline
#         self.lam = 1.16
#         self.point_along_pathline = point_along_pathline if point_along_pathline is not None else 0

#         self.H2_fluid = Fluid(release_temperature, release_pressure, 'H2', diameter=orifice_diameter,
#                               velocity=self.velocity_if_not_sonic, mass_fraction=1)
#         self.ambient_fluid = Fluid(ambient_temperature, ambient_pressure, 'AIR')

#     def run(self):
#         self._point_1()
#         self._point_2()
#         self._point_3()
#         self._point_4()
#         self._integration_zone()
#         self._format_solution()
#         self._separation_distance()

#     def _point_1(self):

#         # enthalpy and entropy at source
#         self.enthalpy_at_0 = cp.PropsSI(['H'], 'P', self.H2_fluid.pressure, 'T', self.H2_fluid.temperature, 'H2')
#         self.entropy_at_0 = cp.PropsSI(['S'], 'P', self.H2_fluid.pressure, 'T', self.H2_fluid.temperature, 'H2')

#         # Function for finding pressure at 1 if flow is choked
#         def error_velocity(pressure):
#             speed_of_sound = cp.PropsSI(['A'], 'P', pressure, 'S', float(self.entropy_at_0), 'H2')
#             enthalpy = cp.PropsSI(['H'], 'P', pressure, 'S', float(self.entropy_at_0), 'H2')
#             if self.enthalpy_at_0 - enthalpy > 0:
#                 velocity_from_energy_conservation = np.sqrt(2 * (self.enthalpy_at_0 - enthalpy))
#             else:
#                 velocity_from_energy_conservation = 0
#             return speed_of_sound - velocity_from_energy_conservation

#         # Find if flow is choked   
#         if self.H2_fluid.pressure > 1.9 * self.ambient_fluid.pressure:
#             if self.velocity_if_not_sonic is not None:
#                 warnings.warn("Flow over specified, release velocity not used")

#             pressure_at_1 = optimize.brentq(error_velocity, self.H2_fluid.pressure, self.ambient_fluid.pressure)
#             self.pressure_at_1 = pressure_at_1
#             temperature_at_1 = cp.PropsSI(['T'], 'P', pressure_at_1, 'S', float(self.entropy_at_0), 'H2')
#             velocity_at_1 = cp.PropsSI(['A'], 'P', pressure_at_1, 'S', float(self.entropy_at_0), 'H2')
#             # Update fluid object with properties at 1
#             self.H2_fluid.update(temperature=temperature_at_1, pressure=pressure_at_1, velocity=velocity_at_1,
#                                  diameter=self.orifice_diameter, choked=True)

#         else:
#             self.choked = False
#             if self.velocity_if_not_sonic is None:
#                 warnings.warn("Velocity required if flow is subsonic")
#             temperature_at_1 = cp.PropsSI(['T'], 'P', self.ambient_fluid.pressure, 'S', float(self.entropy_at_0), 'H2')
#             # Update fluid object with properties at 1
#             self.H2_fluid.update(pressure=self.ambient_fluid.pressure, temperature=temperature_at_1,
#                                  velocity=self.velocity_if_not_sonic, choked=False)

#     def _point_2(self):
#         # Only is choked, if not choked properties stay the same
#         if self.H2_fluid.choked:
#             # from notional nozzle model
#             velocity_at_2 = (self.H2_fluid.diameter ** 2 / 4 * np.pi * (
#                     self.H2_fluid.pressure - self.ambient_fluid.pressure) + self.H2_fluid.mass_flow_rate * self.H2_fluid.velocity) / self.H2_fluid.mass_flow_rate
#             enthalpy_at_1 = cp.PropsSI(['H'], 'P', float(self.H2_fluid.pressure), 'T', float(self.H2_fluid.temperature),
#                                        'H2')
#             enthalpy_at_2 = enthalpy_at_1 + 1 / 2 * self.H2_fluid.velocity ** 2 - 1 / 2 * velocity_at_2 ** 2
#             temperature_at_2 = cp.PropsSI(['T'], 'P', self.ambient_fluid.pressure, 'H', enthalpy_at_2, 'H2')
#             self.H2_fluid.update(pressure=self.ambient_fluid.pressure, temperature=temperature_at_2,
#                                  velocity=velocity_at_2, mass_flow_rate=self.H2_fluid.mass_flow_rate)

#     def _point_3(self):

#         arbitrary_temperature = 47

#         def error_energy_equation(mass_air):
#             mass_at_3 = self.H2_fluid.mass_flow_rate + mass_air
#             mass_fraction_H2_at_3 = self.H2_fluid.mass_flow_rate / mass_at_3
#             enthalpy_H2 = cp.PropsSI(['H'], 'P', float(self.H2_fluid.pressure), 'T', float(arbitrary_temperature), 'H2')
#             enthalpy_air = cp.PropsSI(['H'], 'P', float(self.ambient_fluid.pressure), 'T',
#                                       float(self.ambient_fluid.temperature), 'AIR')
#             enthalpy_mixture = mass_fraction_H2_at_3 * enthalpy_H2 + (1 - mass_fraction_H2_at_3) * enthalpy_air
#             velocity_at_3 = self.H2_fluid.mass_flow_rate * self.H2_fluid.velocity / mass_at_3
#             residual = self.H2_fluid.mass_flow_rate * (
#                     enthalpy_at_2 + 0.5 * self.H2_fluid.velocity ** 2) - mass_at_3 * (
#                                enthalpy_mixture + 0.5 * velocity_at_3 ** 2)
#             return residual, mass_at_3, velocity_at_3, mass_fraction_H2_at_3

#         if self.H2_fluid.temperature < arbitrary_temperature:
#             enthalpy_at_1 = cp.PropsSI(['H'], 'P', float(self.H2_fluid.pressure), 'T', float(self.H2_fluid.temperature),
#                                        'H2')
#             enthalpy_at_2 = enthalpy_at_1 + 1 / 2 * self.H2_fluid.velocity ** 2 - 1 / 2 * self.H2_fluid.velocity ** 2
#             mass_air_entrained = optimize.brentq(lambda x: error_energy_equation(x)[0], -100, 100)
#             mass_at_3 = error_energy_equation(mass_air_entrained)[1]
#             velocity_at_3 = error_energy_equation(mass_air_entrained)[2]
#             mass_fraction_H2_at_3 = error_energy_equation(mass_air_entrained)[3]
#             # Update fluid object
#             self.H2_fluid.update(temperature=arbitrary_temperature, velocity=velocity_at_3,
#                                  pressure=self.ambient_fluid.pressure, mass_flow_rate=mass_at_3,
#                                  mass_fraction=mass_fraction_H2_at_3)

#     def _point_4(self):
#         BE = self.H2_fluid.diameter / np.sqrt(
#             2 * (2 * self.lam ** 2 + 1) / (
#                     self.lam ** 2 * self.H2_fluid.density / self.ambient_fluid.density + self.lam ** 2 + 1))
#         v_cl = self.H2_fluid.velocity
#         Y_cl = self.H2_fluid.mass_fraction * (self.lam ** 2 + 1.) / (2. * self.lam ** 2)
#         enthalpy_ambient = cp.PropsSI(['H'], 'P', self.ambient_fluid.pressure, 'T', self.ambient_fluid.temperature,
#                                       'AIR')
#         Cp_gas = cp.PropsSI(['C'], 'P', self.ambient_fluid.pressure, 'T',
#                             (self.H2_fluid.temperature + self.ambient_fluid.temperature) / 2, 'H2')
#         MW_cl = 1.0 / (Y_cl / self.H2_fluid.molecular_weight + (1.0 - Y_cl) / self.ambient_fluid.molecular_weight)
#         Cp_mix = self.H2_fluid.mass_fraction * Cp_gas + (
#                 1.0 - self.H2_fluid.mass_fraction) * self.ambient_fluid.specific_heat
#         enthalpy_mixture = Cp_mix * self.H2_fluid.temperature
#         enthalpy_cl = enthalpy_ambient + (self.lam ** 2 + 1.) / (2. * self.lam ** 2) * (
#                 enthalpy_mixture - enthalpy_ambient)
#         Cp_cl = Y_cl * Cp_gas + (1.0 - Y_cl) * self.ambient_fluid.specific_heat
#         T_cl = enthalpy_cl / Cp_cl
#         rho_cl = self.ambient_fluid.pressure * MW_cl / (constant.R * T_cl)
#         distance_along_s = 6.2 * self.H2_fluid.diameter
#         x, y, S = 0, 0, 0
#         initial_x = x + distance_along_s * np.cos(self.release_angle)
#         initial_y = y + distance_along_s * np.sin(self.release_angle)
#         self.initial_S = S + distance_along_s
#         self.conditions = [v_cl, BE, rho_cl, Y_cl, self.release_angle, initial_x, initial_y]

#     def _integration_zone(self, max_steps=100000, Smax=np.inf):
#         dS = 500 * self.orifice_diameter
#         r = integrate.ode(self._gov_equations)
#         r.set_integrator('dopri5', atol=1e-6, rtol=1e-6)
#         T, Y = [], []

#         def solout(t, y):
#             T.append(t)
#             Y.append(np.array(y))

#         r.set_solout(solout)
#         r.set_initial_value(self.conditions, self.initial_S)
#         i = 0
#         while r.successful() and r.y[3] > self.min_concentration and i < max_steps and r.t < Smax:
#             r.integrate(r.t + dS)
#             i += 1

#         self.Y = np.array(Y)
#         self.T = np.array(T)

#     def _format_solution(self):
#         MW = self.ambient_fluid.molecular_weight * self.H2_fluid.molecular_weight / (self.Y[:, 3] * (
#                 self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) + self.H2_fluid.molecular_weight)
#         mole_fraction = self.Y[:, 3] * MW / self.H2_fluid.molecular_weight
#         solution = np.append(self.Y, mole_fraction.reshape(mole_fraction.shape[0], 1), axis=1)

#         self.__solution__ = {}

#         for key, val in zip(['V_cl', 'B', 'rho_cl', 'Y_cl', 'theta', 'x', 'y', 'mole_fraction'], solution.T):
#             self.__solution__[key] = val
#         self.__solution__['S'] = self.T

#     def _calculate_entrainment(self, V_cl, B, rho_cl, theta, alpha):
#         FrL = V_cl ** 2 * rho_cl / (constant.g * B * abs(self.ambient_fluid.density - rho_cl))
#         Fr = self.H2_fluid.velocity / np.sqrt(constant.g * self.H2_fluid.diameter * abs(
#             self.ambient_fluid.density - self.H2_fluid.density) / self.H2_fluid.density)
#         if Fr < 268:
#             alpha_buoy = 17.313 - 0.11665 * Fr + 2.0771e-4 * Fr ** 2
#         else:
#             alpha_buoy = 0.97

#         E_buoy = alpha_buoy / FrL * (2 * constant.pi * V_cl * B) * np.sin(theta)
#         BetaA = .28

#         Emom = BetaA * np.sqrt(constant.pi / 4.0 * self.H2_fluid.diameter ** 2 *
#                                self.H2_fluid.density * self.H2_fluid.velocity ** 2 / self.ambient_fluid.density)

#         E = Emom + E_buoy
#         alphatest = E / (2 * constant.pi * V_cl * B)
#         if alphatest > alpha:
#             E = alpha * 2 * constant.pi * B * V_cl
#         return E

#     def _continuity_equation(self, rho_cl, B, V_cl, E):
#         LHScont = np.array([(self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B ** 2,  # d/dS(V_cl)
#                             2 * (self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B * V_cl,  # d/dS(B)
#                             self.lam ** 2 * B ** 2 * V_cl,  # d/dS(rho_cl)
#                             0.,  # d/dS(Y_cl)

#                             0.]) * constant.pi / (self.lam ** 2 + 1)  # d/dS(theta)
#         RHScont = self.ambient_fluid.density * E
#         return LHScont, RHScont

#     def _x_momentum_equation(self, rho_cl, V_cl, theta, B):
#         LHSxmom = np.array(
#             [(2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B ** 2 * V_cl * np.cos(theta),  # d/dS(V_cl)
#              (2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B * V_cl ** 2 * np.cos(theta),  # d/dS(B)
#              self.lam ** 2 * B ** 2 * V_cl ** 2 * np.cos(theta),  # d/dS(rho_cl)
#              0.,  # d/dS(Y_cl)
#              -(2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * (B * V_cl) ** 2 * np.sin(theta) / 2
#              # d/dS(theta)
#              ]) * constant.pi / (2 * self.lam ** 2 + 1)
#         RHSxmom = 0.
#         return LHSxmom, RHSxmom

#     def _y_momentum_equation(self, rho_cl, V_cl, theta, B):
#         LHSymom = np.array(
#             [(2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B ** 2 * V_cl * np.sin(theta),  # d/dS(V_cl)
#              (2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B * V_cl ** 2 * np.sin(theta),  # d/dS(B)
#              self.lam ** 2 * B ** 2 * V_cl ** 2 * np.sin(theta),  # d/dS(rho_cl)
#              0.,  # d/dS(Y_cl)
#              (2 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * (B * V_cl) ** 2 * np.cos(theta) / 2
#              # d/dS(theta)
#              ]) * constant.pi / (2 * self.lam ** 2 + 1)
#         RHSymom = -constant.pi * self.lam ** 2 * constant.g * (rho_cl - self.ambient_fluid.density) * B ** 2
#         return LHSymom, RHSymom

#     def _species_equation(self, rho_cl, Y_cl, B, V_cl):
#         LHSspec = np.array([B * Y_cl * rho_cl,  # d/dS(V_cl)
#                             2 * V_cl * Y_cl * rho_cl,  # d/dS(B)
#                             B * V_cl * Y_cl,  # d/dS(rho_cl)
#                             B * V_cl * rho_cl,  # d/dS(Y_cl)
#                             0.,  # d/dS(theta)
#                             ]) * constant.pi * self.lam ** 2 * B / (self.lam ** 2 + 1)
#         RHSspec = 0
#         return LHSspec, RHSspec


#     def _energy_equation(self, RHScont, rho_cl, V_cl, B, Y_cl, numB=5, numpts=500):
#         h_amb = self.ambient_fluid.specific_heat * self.ambient_fluid.temperature
#         Cp_fluid = cp.PropsSI(['C'], 'P', float(self.H2_fluid.pressure), 'T', float(self.H2_fluid.temperature), 'H2')
#         r = np.append(np.array([0]), np.logspace(-5, np.log10(numB * B), numpts))
#         zero = np.zeros_like(r)
#         V = V_cl * np.exp(-(r ** 2) / (B ** 2))
#         rho = (rho_cl - self.ambient_fluid.density) * np.exp(
#             -(r ** 2) / ((self.lam * B) ** 2)) + self.ambient_fluid.density
#         Y = Y_cl * rho_cl / rho * np.exp(-r ** 2 / (self.lam * B) ** 2)
#         self.MW = self.ambient_fluid.molecular_weight * self.H2_fluid.molecular_weight / (Y * (
#                 self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) + self.H2_fluid.molecular_weight)
#         dYdS = np.array([zero,  # d/dS(V_cl)
#                          (2 * Y ** 2 * self.ambient_fluid.density * r ** 2 * np.exp(r ** 2 / (self.lam * B) ** 2) /
#                           (self.lam ** 2 * B ** 3 * Y_cl * rho_cl)),  # d/dS(B)
#                          Y ** 2 * self.ambient_fluid.density * (np.exp(r ** 2 / (self.lam * B) ** 2) - 1) / (
#                                  Y_cl * rho_cl ** 2),
#                          # d/dS(rho_cl)
#                          Y / Y_cl,  # d/dS(Y_cl)
#                          zero])  # d/dS(theta)
#         dMWdS = (self.MW * (self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) / (
#                 self.H2_fluid.molecular_weight * (Y - 1) - self.ambient_fluid.molecular_weight * Y)) * dYdS
#         Cp = Y * (Cp_fluid - self.ambient_fluid.specific_heat) + self.ambient_fluid.specific_heat
#         dCpdS = (Cp_fluid - self.ambient_fluid.specific_heat) * dYdS
#         rhoh = self.ambient_fluid.pressure / constant.R * self.MW * Cp
#         drhohdS = self.ambient_fluid.pressure / constant.R * (self.MW * dCpdS + Cp * dMWdS)
#         dVdS = np.array([V / V_cl,  # d/dS(V_cl)
#                          2 * V * r ** 2 / B ** 3,  # d/dS(B)
#                          zero,  # d/dS(rho_cl)
#                          zero,  # d/dS(Y_cl)
#                          zero])  # d/dS(theta)

#         LHSener = 2 * constant.pi * integrate.trapz(V * drhohdS * r + rhoh * dVdS * r, r)
#         LHSener += [
#             constant.pi / (6 * self.lam ** 2 + 2) * (
#                     3 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * B ** 2 * V_cl ** 2,
#             # d/dS(V_cl)
#             constant.pi / (9 * self.lam ** 2 + 3) * (
#                     3 * self.lam ** 2 * rho_cl + self.ambient_fluid.density) * V_cl ** 3 * B,
#             # d/dS(B)
#             constant.pi / (6 * self.lam ** 2 + 2) * self.lam ** 2 * B ** 2 * V_cl ** 3,  # d/dS(rho_cl)
#             0.,  # d/dS(Y_cl)
#             0.]  # d/dS(theta)

#         RHSener = h_amb * RHScont
#         return LHSener, RHSener

#     def _gov_equations(self, S, ind_vars, alpha=0.082):
#         [V_cl, B, rho_cl, Y_cl, theta, x, y] = ind_vars
#         E = self._calculate_entrainment(V_cl, B, rho_cl, theta, alpha)
#         # governing equations:

#         LHScont, RHScont = self._continuity_equation(rho_cl, B, V_cl, E)
#         LHSxmom, RHSxmom = self._x_momentum_equation(rho_cl, V_cl, theta, B)
#         LHSymom, RHSymom = self._y_momentum_equation(rho_cl, V_cl, theta, B)
#         LHSspec, RHSspec = self._species_equation(rho_cl, Y_cl, B, V_cl)
#         LHSener, RHSener = self._energy_equation(RHScont, rho_cl, V_cl, B, Y_cl, numB=5, numpts=500)

#         LHS = np.array([LHScont,
#                         LHSxmom,
#                         LHSymom,
#                         LHSspec,
#                         LHSener
#                         ])
#         RHS = np.array([RHScont,
#                         RHSxmom,
#                         RHSymom,
#                         RHSspec,
#                         RHSener])

#         dz = np.append(np.linalg.solve(LHS, RHS), np.array([np.cos(theta), np.sin(theta)]), axis=0)
#         return dz

#     def centerline_velocity_plot(self):
#         fig, ax = plt.subplots(figsize=(6, 4))
#         ax.plot(self.__solution__['S'], self.__solution__['V_cl'], linewidth=2)
#         ax.set_xlabel('S (m)')
#         ax.set_ylabel('V_cl (m/s)')
#         ax.set_title('Centerline velocity along path')
#         return fig

#     def centerline_mass_concentration_plot(self):
#         fig, ax = plt.subplots(figsize=(6, 4))
#         ax.plot(self.__solution__['S'], self.__solution__['Y_cl'], linewidth=2)
#         ax.set_xlabel('S (m)')
#         ax.set_ylabel('Y_cl')
#         ax.set_title('Centerline mass concentration along path')
#         return fig

#     def theta_plot(self):
#         fig, ax = plt.subplots(figsize=(6, 4))
#         ax.plot(self.__solution__['S'], self.__solution__['theta'], linewidth=2)
#         ax.set_xlabel('S (m)')
#         ax.set_ylabel('Theta (rad)')
#         ax.set_title('Curve angle')
#         return fig

#     def concentration_profile_plot(self):
#         nums = np.linspace(30, len(self.__solution__['S']) - 1, 10)
#         nums = np.round(nums).astype(int)
#         r = np.linspace(-2 * self.__solution__['B'], 2 * self.__solution__['B'], 100).reshape(100, len(
#             self.__solution__['S']))
#         V = self.__solution__['V_cl'].T * np.exp(-r ** 2 / self.__solution__['B'] ** 2) / 50
#         rho_cl = self.__solution__['rho_cl']
#         rho = (rho_cl - self.ambient_fluid.density) * np.exp(
#             -r ** 2 / (self.__solution__['B'] ** 2 * self.lam ** 2)) + self.ambient_fluid.density
#         Y_concentration = 1 / rho * rho_cl * self.__solution__['Y_cl'] * np.exp(
#             -r ** 2 / (self.__solution__['B'] ** 2 * self.lam ** 2))
#         R = self.rotation_matrix(self.__solution__['theta'])
#         # multiply by 200 so profiles don't look so small
#         transformed_coords_cons = np.array([r, Y_concentration * 200]).T @ R.T  # + xy_coords[:, np.newaxis]
#         fig, ax = plt.subplots(figsize=(6, 4))
#         plot = plt.fill(transformed_coords_cons[nums, :, 0].T + self.__solution__['x'][nums],
#                         transformed_coords_cons[nums, :, 1].T + self.__solution__['y'][nums], color='red', lw=1,
#                         facecolor='pink', alpha=.5)
#         ax.set_xlabel('x (m)')
#         ax.set_ylabel('y (m)')
#         ax.set_title('Qualitative concentration profile along path')
#         ax.legend([plot[0]], ['H2 concentration profile'])
#         return fig

#     def _contour_data(self):
#         iS = np.arange(len(self.__solution__['S']))
#         poshalf = np.logspace(-5, np.log10(3 * np.max(self.__solution__['B'])))
#         r = np.concatenate((-1.0 * poshalf[::-1], [0], poshalf))
#         r, iS = np.meshgrid(r, iS)
#         B = self.__solution__['B'][iS]
#         rho_cl = self.__solution__['rho_cl'][iS]
#         Y_cl = self.__solution__['Y_cl'][iS]
#         rho = (rho_cl - self.ambient_fluid.density) * np.exp(
#             -r ** 2 / (B ** 2 * 1.16 ** 2)) + self.ambient_fluid.density
#         Y_concentration = 1 / rho * rho_cl * Y_cl * np.exp(-r ** 2 / (B ** 2 * self.lam ** 2))
#         MW = self.ambient_fluid.molecular_weight * self.H2_fluid.molecular_weight / (Y_concentration * (
#                 self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) + self.H2_fluid.molecular_weight)
#         X_concentration = Y_concentration * MW / self.H2_fluid.molecular_weight
#         x = self.__solution__['x'][iS] + r * np.sin(self.__solution__['theta'][iS])
#         y = self.__solution__['y'][iS] - r * np.cos(self.__solution__['theta'][iS])
#         return x, y, X_concentration

#     def _separation_distance(self):
#         x, y, X_concentration = self._contour_data()
#         contour = plt.contour(x, y, X_concentration, levels=[self.contour_of_interest], colors='white', alpha=1,
#                               linewidths=4)
#         plt.close()
#         line = np.array(contour.allsegs)
#         line = line[:, 0, :, :].reshape(np.shape(line)[2], 2)

#         if self.release_angle <= np.pi / 2 and self.release_angle >= 0:
#             x_arg = np.argmax(line[:, 0])
#             y_arg = np.argmax(line[:, 1])

#         elif self.release_angle > np.pi / 2 and self.release_angle <= np.pi:
#             x_arg = np.argmin(line[:, 0])
#             y_arg = np.argmax(line[:, 1])

#         elif self.release_angle > np.pi and self.release_angle <= 3 / 2 * np.pi:
#             x_arg = np.argmin(line[:, 0])
#             y_arg = np.argmin(line[:, 1])

#         elif self.release_angle > 3 / 2 * np.pi and self.release_angle <= 2 * np.pi:
#             x_arg = np.argmax(line[:, 0])
#             y_arg = np.argmin(line[:, 1])

#         else:
#             x_arg = np.argmax(line[:, 0])
#             y_arg = np.argmax(line[:, 1])

#         self.max_x_coords = line[x_arg, :]
#         self.max_y_coords = line[y_arg, :]

#     def contour_plot_1(self):
#         x, y, X_concentration = self._contour_data()
#         fig, ax = plt.subplots()
#         cont = plt.contourf(x, y, X_concentration, levels=np.linspace(.00001, 1, 100), cmap=cm.coolwarm, alpha=0.7)
#         cont_LFL = ax.contour(x, y, X_concentration, levels=[self.contour_of_interest], colors='white', alpha=1,
#                               linewidths=4)
#         ax.set_title('Contour plot 1, along path')
#         fig.colorbar(cont)
#         plt.xlabel('x (m)')
#         plt.ylabel('y (m)')
#         line = np.array(cont_LFL.allsegs)
#         line = line[:, 0, :, :].reshape(np.shape(line)[2], 2)
#         scale_factor = 1.2

#         ax.axvline(x=self.max_x_coords[0], linewidth=2, color='white', label='separation distance')
#         ax.axhline(y=self.max_y_coords[1], linewidth=2, color='white')
#         ax.scatter(self.max_x_coords[0], self.max_y_coords[1], color='red', s=150, zorder=3, marker='*')
#         ax.legend()

#         if self.Y_contour_range[0] is not None:
#             ax.set_ylim(self.Y_contour_range[0], self.Y_contour_range[1])
#         else:
#             ax.set_ylim(np.min(line[:, 1] * scale_factor), np.max(line[:, 1]) * scale_factor)

#         if self.X_contour_range[0] is not None:
#             ax.set_xlim(self.X_contour_range[0], self.X_contour_range[1])
#         else:
#             ax.set_xlim(np.min(line[:, 0] * scale_factor), np.max(line[:, 0]) * scale_factor)
#         ax.clabel(cont_LFL, inline=True, fontsize=20)
#         return fig

#     def contour_plot_2(self):
#         x, y, X_concentration = self._contour_data()
#         fig, ax = plt.subplots()
#         cont = ax.contour(x, y, X_concentration, levels=[0.02, 0.04, 0.06, 0.08], cmap=cm.coolwarm, alpha=0.7,
#                           linewidths=4)
#         line = np.array(cont.allsegs[0])
#         line = line[0, :, :].reshape(np.shape(line)[1], 2)
#         scale_factor = 1.2

#         ax.set_xlim(np.min(line[:, 0] * scale_factor), np.max(line[:, 0]) * scale_factor)
#         ax.set_ylim(np.min(line[:, 1] * scale_factor), np.max(line[:, 1]) * scale_factor)
#         ax.set_xlabel('x (m)')
#         ax.set_ylabel('y (m)')
#         ax.clabel(cont, inline=True, fontsize=20)
#         ax.set_title('Contour plot 2, along path')
#         return fig

#     def contour_plot_3(self):
#         fig, ax = plt.subplots()
#         S_idx = np.argmin(np.abs(self.point_along_pathline - self.__solution__['S']))
#         x = np.linspace(-5, 5, num=1500)
#         y = np.linspace(-5, 5, num=1500)
#         x, y = np.meshgrid(x, y)
#         B = self.__solution__['B'][S_idx]
#         rho_cl = self.__solution__['rho_cl'][S_idx]
#         Y_cl = self.__solution__['Y_cl'][S_idx]
#         rho = (rho_cl - self.ambient_fluid.density) * np.exp(
#             -(x ** 2 + y ** 2) ** 2 / (B ** 2 * self.lam ** 2)) + self.ambient_fluid.density
#         Y_concentration = 1 / rho * rho_cl * Y_cl * np.exp(-(x ** 2 + y ** 2) ** 2 / (B ** 2 * self.lam ** 2))
#         MW = self.ambient_fluid.molecular_weight * self.H2_fluid.molecular_weight / (Y_concentration * (
#                 self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) + self.H2_fluid.molecular_weight)
#         X_concentration = Y_concentration * MW / self.H2_fluid.molecular_weight
#         cont = ax.contourf(x, y, X_concentration, cmap=cm.coolwarm, levels=np.linspace(.00001, 1, 100), alpha=0.7)
#         cont_LFL = ax.contour(x, y, X_concentration, levels=[self.contour_of_interest], colors='white', alpha=1,
#                               linewidths=4)
#         fig.colorbar(cont)
#         line = np.array(cont_LFL.allsegs)
#         line = line[:, 0, :, :].reshape(np.shape(line)[2], 2)
#         scale_factor = 1.2
#         ax.set_xlim(np.min(line[:, 0] * scale_factor), np.max(line[:, 0]) * scale_factor)
#         ax.set_ylim(np.min(line[:, 1] * scale_factor), np.max(line[:, 1]) * scale_factor)
#         ax.set_xlabel('r (m)')
#         ax.set_ylabel('r (m)')
#         ax.set_title('Contour plot 3, {} m along pathline, perpendicular to pathline'.format(
#             np.round(self.__solution__['S'][S_idx], 3)))
#         ax.set_aspect('equal')
#         ax.clabel(cont_LFL, inline=True, fontsize=15)
#         return fig

#     def rotation_matrix(self, theta):
#         return np.array([[np.cos(theta - np.pi / 2), -np.sin(theta - np.pi / 2)],
#                          [np.sin(theta - np.pi / 2), np.cos(theta - np.pi / 2)]])


# class OtherJetModel(JetModel):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
    
#     def _gov_equations(self, S, ind_vars, alpha=0.082):
#         [V_cl, B, rho_cl, theta, x, y] = ind_vars
#         E = self._calculate_entrainment(V_cl, B, rho_cl, theta, alpha)
#         # governing equations:

#         LHScont, RHScont = self._continuity_equation(rho_cl, B, V_cl, E)
#         LHSxmom, RHSxmom = self._x_momentum_equation(rho_cl, V_cl, theta, B)
#         LHSymom, RHSymom = self._y_momentum_equation(rho_cl, V_cl, theta, B)
#         LHSspec, RHSspec = self._species_equation(rho_cl, B, V_cl)

#         LHScont = np.delete(LHScont, 3, axis=0)
#         LHSxmom = np.delete(LHSxmom, 3, axis=0)
#         LHSymom = np.delete(LHSymom, 3, axis=0)

#         LHS = np.array([LHScont,
#                         LHSxmom,
#                         LHSymom,
#                         LHSspec,
#                         ])
#         RHS = np.array([RHScont,
#                         RHSxmom,
#                         RHSymom,
#                         RHSspec,
#                         ])
#         dz = np.append(np.linalg.solve(LHS, RHS), np.array([np.cos(theta), np.sin(theta)]), axis=0)
#         return dz

#     def _species_equation(self, rho_cl, B, V_cl):
#         LHSspec = np.array([self.lam ** 2 * B ** 2 / (1 + self.lam ** 2) * (self.ambient_fluid.density - rho_cl),
#              2 * B * V_cl * self.lam ** 2 / (1 + self.lam ** 2) * (self.ambient_fluid.density - rho_cl),  
#              -V_cl * self.lam ** 2 * B ** 2 / (1 + self.lam ** 2),  
#              0])
#         RHSspec = 0
#         return LHSspec, RHSspec

#     def _integration_zone(self, max_steps=100, Smax=np.inf):
#         dS = 500 * self.orifice_diameter
#         r = integrate.ode(self._gov_equations)
#         r.set_integrator('dopri5', atol=1e-6, rtol=1e-6)
#         T, Y = [], []
#         del (self.conditions[3])

#         def solout(t, y):
#             T.append(t)
#             Y.append(np.array(y))

#         r.set_solout(solout)
#         r.set_initial_value(self.conditions, self.initial_S)
#         i = 0
#         y_cl = np.inf # arbitrary

#         radius = np.linspace(-10, 10, 100)
#         while r.successful() and y_cl > self.min_concentration and i < max_steps and r.t < Smax:
#             r.integrate(r.t + dS)
#             rho = (r.y[2] - self.ambient_fluid.density) * np.exp(
#                 -radius ** 2 / (r.y[1] ** 2 * self.lam ** 2)) + self.ambient_fluid.density
#             Y_concentration = self.H2_fluid.molecular_weight / (
#                         self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) * (
#                                           self.ambient_fluid.density / rho - 1)
#             y_cl = Y_concentration[50]
#             i += 1

#         self.Y = np.array(Y)
#         self.T = np.array(T)

#         rho_cl = self.Y[:, 2]
#         radius = np.linspace(-2 * self.Y[:, 1], 2 * self.Y[:, 1], 100).reshape(100, self.Y.shape[0])
#         rho = (rho_cl - self.ambient_fluid.density) * np.exp(
#             -radius ** 2 / (self.Y[:, 1] ** 2 * self.lam ** 2)) + self.ambient_fluid.density
#         Y_concentration = self.H2_fluid.molecular_weight / (
#                     self.ambient_fluid.molecular_weight - self.H2_fluid.molecular_weight) * (
#                                       self.ambient_fluid.density / rho - 1)
#         Y_cl = Y_concentration[50, :]
#         self.Y = np.concatenate((self.Y[:, 0:3], Y_cl[:, np.newaxis], self.Y[:, 3:]), axis=1)

#================================END MATPLOTLIB VERSION OF THE CODE===================================
#=====================================================================================================