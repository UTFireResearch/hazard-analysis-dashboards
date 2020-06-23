import numpy as np
import cantera as ct

RR = 8.314                      #Reynolds number
Patm = 101000                   #Standard atmosphere in Pa
Patmpsi = Patm * 0.000145038    #Standard atmosphere in psi

#Establish class to hold attributes for input fuel parameters
class Fuel():
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def info(self):
        [print(f" {k}  \t \t  {v}") for k, v in self.__dict__.items()]


#Establish class to hold attributes for input room and vent parameters
class Geometry():
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def info(self):
        [print(f" {k}  \t \t  {v}") for k, v in self.__dict__.items()]

class Vent():
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

    def areaV():

        #Standard Air Composition Attribute
        air_species = self.air
        #Fuel Gas Composition Passed Into Vent Object on creation
        fuel_species = self.fuel
        #Equivalence Ratio
        phi = self.phi

        # Temperatures and Pressures
        Patm = self.P  # Initial Pressure
        T = self.T  # Initial unburned gas temperature K
        P1 = Patm  # Initial Pressure
        Pa = Patm  # Exit pressure outside vent
        # Tu = T  # Unburned gas temperature
        T1 = T  # Initial Temperature

        #Geometry parameters
        L = self.Length
        W = self.Width
        H = self.Height
        #Face Areas
        Aw1 = L*H
        Aw2 = D*H
        Aw3 = D*L
        #Total Surface Area
        As = 2*Aw1 + 2*Aw2 + Aw3
        #Hydraulic Diameter
        Dhe = 4*(Aw2/(2*D+2*H))
        #Area Blockage Ratio
        Br = self.Block
        #Reduced Pressure
        P_red = self.reduced

        #Vent Drag Coefficient
        Cd = self.Cd
        #Vent Static Activation Pressures
        P_stat = self.P_stat
        #Unburned Gas-Air Mixture Sonic Flow Mass Flux(kg/m^2-s)
        Gu = 230.1

        #Flame speed
        Su = self.Su

        #Cantera Objects
        carbon = ct.Solution('graphite.xml')
        # Calls Gas Properties from Gri-MECH -- creates burned gas object
        gas_b = ct.Solution('gri30.xml', 'gri30_mix')
        # Calls Gas Properties from Gri-MECH -- creates unburned object
        gas_u = ct.Solution('gri30.xml', 'gri30_mix')

        mix_phases_b = [(gas_b, 1.0), (carbon, 0.0)]  # Burned Mixture
        mix_phases_u = [(gas_u, 1.0), (carbon, 0.0)]  # Unburned Mixture

        gas_b.set_equivalence_ratio(phi, fuel_species, air_species)
        gas_u.set_equivalence_ratio(phi, fuel_species, air_species)

        gas_b.TP = T, Patm
        gas_u.TP = T, Patm

        #Unburned gas-air mixture speed of sound (m/s):
        au = equilSoundSpeeds(gas)[0]

        rho_u = gas_b.density
        mu_u = gas_b.viscosity

        unburned = ct.Mixture(mix_phases_u)  # noqa
        burned = ct.Mixture(mix_phases_b)

        burned.equilibrate('HP', solver='gibbs', max_steps=1000)
        gamma_b = gas_b.cp/gas_b.cv


        #------------VENT AREA FUNCTION FROM AUSTIN'S SCRIPT-------------------
        Dv - math.sqrt((Av1/Vent_Number))

        #Reynolds number of flame through structure:
        Re_flame = rho_u*Su*(0.5*Dhe)/mu_u
        #Phi 1: Based on Reynolds Number of Flame Front:
        phi_1 = max(1, (Re_flame/4000)**0.39)

        #Maximum Velocity through Vent (m/s):
        uv = min(math.sqrt(Pred*2*10**5/rho_u),au)

        #Reynolds number through vent
        Re_vent = 0.5*rho_u*uv*Dv/mu_u

        #Phi 2: Based on Reynolds Number through Vent:
        beta1 = 1.23
        beta2 = 2.37*10**-3
        phi_2 = max(1, beta1*(Re_vent/10**6)**((beta2/Su)**0.5))

        #Lambda 0:
        Lambda_0=phi_1*phi_2

        #Lambda 1 Based on Obstructed surface area (m^2):
        Aobs = 0.3*As

        #Obstruction Correction Factor
        if Aobs < 0.2*As:
            Lambda_1=Lambda_0
        elif Aobs >= 0.2*As:
            Lambda_1=Lambda_0*math.exp(math.sqrt((Aobs/As)-0.2))

        #L/D
        L_D = L/Dhe


        #Solving for Lambda:
        if L_D < 2.5:
            Lambda = Lambda_1
        elif L_D >= 2.5:
            Lambda = Lambda_1*(1+((L_D/2.5)-1)**2)

        #L/D Correction Factor
        if L_D > 5:
            print ("L/D Above 5 see NFPA 68 Chapter 9")
        elif Pmax > 10:
            print ("Pmax Above 10 bar-g see NFPA 68")

        #Solving for vent size:
        C = (0.5*Su*rho_u*Lambda/(Gu*Cd))*(((Pmax+1)/(Po+1))**(1/gamma_b)-1)*(Po+1)**0.5
        delta = (((Pstat+1)/(Po+1))**(1/gamma_b)-1)/(((Pmax+1)/(Po+1))**(1/gamma_b)-1)

        #Pred Corrction Factor
        if Pred <= 0.5:
            Avo = As*C/math.sqrt(Pred)
        elif Pred > 0.5:
            Avo = (As*Su*rho_u*Lambda/(Gu*Cd))*(1-((Pred+1)/(Pmax+1))**(1/gamma_b))/(((Pred+1)/(Pmax+1))**(1/gamma_b)-delta)
        return(Avo)


    #Unburned Gas-Air Mixture Speed of Sound (m/s):
    def equilSoundSpeeds(gas, rtol=1.0e-6, maxiter=5000):

        # Set the gas to equilibrium at its current T and P
        gas.equilibrate('TP', rtol=rtol, maxiter=maxiter)

        # save properties
        s0 = gas.s
        p0 = gas.P
        r0 = gas.density

        # Perturb the pressure
        p1 = p0*1.0001

        # Set the gas to a state with the same entropy and composition but
        # The perturbed pressure
        gas.SP = s0, p1

        # Now equilibrate the gas holding S and P constant
        gas.equilibrate('SP', rtol=rtol, maxiter=maxiter)

        # Equilibrium sound speed
        aequil = math.sqrt((p1 - p0)/(gas.density - r0))
        print('executed')
        return aequil,
