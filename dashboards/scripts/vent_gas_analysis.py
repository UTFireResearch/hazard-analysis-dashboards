# -*- coding: utf-8 -*-
"""
Created on Jan 3 2019

@author: erik archibald & Austin Baird
"""

import cantera as ct
import numpy as np
import pandas as pd

fuel_species = 'H2:1'  # H2
# fuel_species = {'H2':1}  # Hydrogen Fuel
# fuel_species = 'C3H8:1'  # Propane
# fuel_species = 'CO:0.5, H2:0.5'  # H2 CO Mix
# fuel_species = 'CH4:1'  # CH4
# # 50 Percent Charge
# fuel_species = ('CO2:0.011502545, CO:0.001180986, H2:0.00984, ',
#                 'CH4:0.00189584 C2H4:0.001874703, C2H6:0.000997333, '
#                 'C3H8:0.005483636')
# # 100 Percent Charge C
# fuel_species = ('CO2:0.033698864, CO:0.023411161, H2:0.0283925, '
#                 'CH4:0.00654975, C2H4:0.002303411, C2H6:0.001314667, '
#                 'C3H8:0.009136364')
# # 150 Percent Charge
# fuel_species = ('CO2:0.0563445, CO:0.0601125, H2:0.073062, CH4:0.0201966, '
#                 'C2H4:0.027186557, C2H6:0.0035904, C3H8:0.011972727')

np.set_printoptions(suppress=True, precision=3)

# Open spreadsheet of literature gas compositions
dfo = pd.read_excel('VentGasLitReview.xlsx', skiprows=1)

# Choose what you want to run
# Only execute for gases where execute = Yes
df = dfo.loc[dfo['Execute'] == 'Yes']
Do_Flamespeed = False  # This takes a long time
Do_Pmax = True
Do_LFL = False

# Known gases in Cantera
gas_list = ['CO2', 'CO', 'H2', 'CH4', 'C2H4',
            'C2H6', 'C3H8', 'N2', 'O2', 'CH3OH']

# Cantera setup
Pi = 101000  # Initial pressure Pa
Ti = 300  # Initial unburned gas temperature K
carbon = ct.Solution('graphite.xml')
# Calls Gas Properties from Gri-MECH
gas = ct.Solution('gri30.xml', 'gri30_mix')

# MAIN LOOP Do calculations for each row of gas data
for index, row in df.iterrows():
    gas_comp = row[gas_list].fillna(0).values
    fuel = dict(zip(gas_list, row[gas_list].fillna(0).values))
    fuel['C3H8'] = 100 - sum(gas_comp) + fuel['C3H8']

    # Calculate Laminar Flamespeed for different equivalence ratios (phi)
    if Do_Flamespeed:
        for phi in np.arange(0.5, 1.6, 0.05):
            try:
                gas.set_equivalence_ratio(phi, fuel, 'O2:1.0, N2:3.76')
                mix = ct.Mixture([(gas, 1.0), (carbon, 0.0)])
                mix.T = Ti
                mix.P = Pi

                # Laminar Flame Speed
                # A freely-propagating flat flame
                f = ct.FreeFlame(gas, width=5)
                # Energy equation enabled
                f.energy_enabled = True
                f.set_max_time_step(50000)
                f.set_refine_criteria(ratio=2.0, slope=0.05, curve=0.05)
                # Solve with multi or mix component transport properties
                f.transport_model = 'Mix'
                f.solve(loglevel=1, auto=True, refine_grid=True)  #
                dfo.loc[index, 'SL_' + str(phi)] = f.u[0]  #
                print('Flamespeed Done! ', f.u[0])
            except Exception:
                print('ERROR! Something went wrong')

    # Calculate Maximum Pressure (Pmax) for different equivalence ratios (phi)
    if Do_Pmax:
        for phi in np.arange(0.5, 1.75, 0.05):
            try:
                gas.set_equivalence_ratio(phi, fuel, 'O2:1.0, N2:3.76')
                mix = ct.Mixture([(gas, 1.0), (carbon, 0.0)])
                mix.T = Ti
                mix.P = Pi
                # Adiabatic Constant Volume
                mix.equilibrate('UV')
                print(mix.P)
                dfo.loc[index, 'Pm_' + str(phi)] = mix.P / Pi
                print('Pmax Done! ', mix.P / Pi)
            except Exception:
                print("ERROR!")

    if Do_LFL:
        print('Add LFL code here')
    # TODO UPDATE LFL CODE

dfo.to_csv('Literature_Gas_Analysis.csv')
