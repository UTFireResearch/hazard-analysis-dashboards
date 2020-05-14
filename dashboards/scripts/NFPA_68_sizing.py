#NFPA 68 Gas Deflagration Vent Calculator
#Disclamer- Use of this code is solely the responsibility of the user

import cantera as ct
import math

#User input function
#Laminar Flame Speed (m/s):
Su = 0.40

#Maximum overpressure (bar-g):
Pmax = 8.6

#Equivalence Ratio
phi = 1.0

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
    return aequil,


gas = ct.Solution('gri30.xml','gri30_mix')

# Calls Gas Properties from Gri-MECH
carbon = ct.Solution('graphite.xml')
mix_phases = [(gas, 1.0),(carbon, 0.0)] # Burned Mixture
gas.set_equivalence_ratio(phi, 'H2:0.3,CH4:0.2,CO:0.1,CO2:0.4', 'O2:1,N2:3.76')
T = 300.0
gas.TP = T, ct.one_atm

#Unburned gas-air mixture speed of sound (m/s):
au = equilSoundSpeeds(gas)[0]

#Ratio of Specific Heats for Burned gas-air mixture
gas_b = ct.Solution('gri30.xml','gri30_mix')

#Calls Gas Properties from Gri-MECH
carbon = ct.Solution('graphite.xml')
mix_phases_b = [(gas_b, 1.0),(carbon, 0.0)]

#Burned Mixture
Pi = 101000 #Initial pressure Pa
Ti = 300 #Initial unburned gas temperature K
gas_b.TP = Ti,Pi
gas_b.set_equivalence_ratio(phi, 'H2:1', 'O2:1.0, N2:3.76')

#Mass Density of Unburned Gas-Air Mixture (kg/m^3):
rho_u = gas_b.density

#Unburned gas-air mixture dynamic viscosity (kg/m-s):
mu_u = gas_b.viscosity

#Suppress the next two lines for unburned data
burned = ct.Mixture(mix_phases_b)

#Equilibrate the mixture adiabatically at constant P
burned.equilibrate('HP', solver='gibbs', max_steps=1000)
gamma_b = gas_b.cp/gas_b.cv #Suppress for unburned data

#Structure Surface Area (m^2):

#Length (m):
L = 24.4

#Depth (m):
D = 30.5

#Height (m):
H = 6.1

#Side Walls
Aw1 = L*H

#Front and Rear Walls
Aw2 = D*H

#Roof and Floor:
Aw3 = D*L

#Total Surface Area
As = 2*Aw1 + 2*Aw2 + Aw3

#Reduced Pressure 2/3 structure ultimate strength (bar-g):
Pred = 0.047

#Intial Pressure (bar-g):
Po = 0.01325

#Static activation pressure of the venting device (bar-g):
Pstat = .04

#Unburned Gas-Air Mixture Sonic Flow Mass Flux(kg/m^2-s)
Gu = 230.1

#Vent flow discharge coefficient
#Assume 0.7 if vent area is no bigger than wall area, other wise 0.8:
Cd = 0.7

#Hydraulic Diameter (m):
Dhe = 4*(Aw2/(2*D+2*H))

#print(Dhe)

#Determining Turbulent Factor:

#Vent diameter: Needs to be iterated based off of

#Assumed number of vents and vent area

#Initial assumption 10 vents with a total area of 90% of wall

def ventarea(Av1):
    Dv = math.sqrt((Av1/Vent_Number))
    
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


#Initial vent area (m^2):
Vent_Number = 10
Vent_Percent = 0.5
Av1 = Vent_Percent*(Aw1)

#print("Av1", Av1)
Avg = 0.001
Avo = 0

while 100*abs(Avo-Avg)/(0.5*(Avo+Avg)) > 1:

    Avo = ventarea(Av1)
    Avg = Av1
    Av1 = Avo
    #print("Avo", Avo)

print("Vent Size Required", Avo, "m^2")

print("Available Surface Area", As, "m^2")


if Avo > 0.5*As:
    print("Warning: Vent Size Exceeds Available Surface Area")
