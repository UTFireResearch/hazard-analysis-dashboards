# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 10:38:16 2019

@author: erik
"""

import cantera as ct
import pandas as pd
import numpy as np
import collections
import os.path as op

import plotly.io as pio
import plotly.figure_factory as ff
import time

pio.renderers.default = "browser"
# Remove extra leading /
pio.orca.config._constants['plotlyjs'] = pio.orca.config.plotlyjs[1:]


def makeAxis(title, tickangle):
    return {
        'title': title,
        'titlefont': {'size': 20},
        'tickangle': tickangle,
        'tickfont': {'size': 15},
        'tickcolor': 'rgba(0,0,0,0)',
        'ticklen': 5,
        'showline': True,
        'showgrid': True
    }


# Setup Cantera
Pi = 101000  # Initial pressure Pa
Ti = 300  # Initial unburned gas temperature K
carbon = ct.Solution('graphite.xml')
# Calls Gas Properties from Gri-MECH
gas = ct.Solution('gri30.xml', 'gri30_mix')
mix = ct.Mixture([(gas, 1.0), (carbon, 0.0)])

fuel10Ah = {'CO2': 44, 'CO': 15, 'H2': 31, 'CH4': 6, 'C3H8': 4}
# 100 Percent Charge C
fuelSom100pct = {'CO2': 30, 'CO': 23, 'H2': 28, 'CH4': 6, 'C2H6': 1, 'C3H8': 4}
# LFP 100 SOC Golubkov 2015 Ethylene binned to Propane
fuelLFP = {'CO2': 48.3, 'CO': 9.1, 'H2': 29.4,
           'CH4': 5.4, 'C2H6': 0.5, 'C3H8': 7.2}

air = {'N2': 3.76, 'O2': 1}

fuel = fuelLFP

data_path = op.join(op.dirname(__file__),
                    'example_data', 'TempCriteriaData.xlsx')
dfTempCrit = pd.read_excel(data_path, index_col=0)

gaslist = ['H2', 'CO', 'CH4', 'C2H6', 'C3H8']
gaslistinert = ['H2O', 'CO2', 'N2']
gaslistfull = ['H2', 'CO', 'CH4', 'C2H6', 'C3H8', 'H2O', 'CO2', 'N2', 'O2']


# Determine Tblend Temperature for given gas mixture
def Tblend(mixx):
    mx = collections.defaultdict(lambda: 0, mixx)
    mx = {key: mx[key] for key in gaslist}
    total = sum([mx[key] for key in gaslist])
    alpha = [mx[key] / total for key in mx]
    Tui = [dfTempCrit.loc[key]['Tu'] for key in gaslist]
    Tli = [dfTempCrit.loc[key]['Tu'] for key in gaslist]
    Tl = np.dot(alpha, Tli)
    Tu = np.dot(alpha, Tui)
    return Tl, Tu


# Run Equilibrium
def Eq(fuel, phi):
    gas = ct.Solution('gri30.xml', 'gri30_mix')
    gas.set_equivalence_ratio(phi, fuel, air)
    mix = ct.Mixture([(gas, 1.0), (carbon, 0.0)])
    mix.T = Ti
    mix.P = Pi
    mix.equilibrate('HP')
    print(mix.T)
    Xf = 1 - sum(mix.phase(0)['N2', 'O2'].X)
    Xff = 1 - sum(mix.phase(0)['N2', 'O2', 'H2O', 'CO2'].X)
    Xair = 1 - Xf
    dResult = {'phi': phi, 'Tad': mix.T, 'Xf': Xf, 'Xff': Xff,
               'air': Xair, 'O2': mix.phase(0)['O2'].X}
    return dResult


def Eqq(X):
    gas = ct.Solution('gri30.xml', 'gri30_mix')
    gas.X = X
    mix = ct.Mixture([(gas, 1.0), (carbon, 0.0)])
    phi = gas.get_equivalence_ratio()
    mix.T = Ti
    mix.P = Pi
    mix.equilibrate('HP')
    Xf = 1 - sum(mix.phase(0)['N2', 'O2'].X)
    Xff = 1 - sum(mix.phase(0)['N2', 'O2', 'H2O', 'CO2'].X)
    Xair = 1 - Xf
    dResult = {'phi': phi, 'Tad': mix.T, 'Xf': Xf, 'Xff': Xff,
               'air': Xair, 'O2': mix.phase(0)['O2'].X}
    return dResult


df = pd.DataFrame(columns=['phi', 'Tad', 'Xf', 'Xff', 'air', 'O2'])


# Fixes dictionary of gas species
def fixDict(Od):
    dd = {}
    factor = 1.0 / sum(Od.values())
    for k in Od:
        if Od[k] * factor > 0.001:
            dd[k] = Od[k] * factor

    factor = 1.0 / sum(dd.values())
    for k in dd:
        dd[k] = dd[k] * factor

    dd = collections.defaultdict(lambda: 0, dd)
    return dd


def doAnalysis(fuel):
    gas.set_equivalence_ratio(1.0, fuel, air)
    mix = ct.Mixture([(gas, 1.0), (carbon, 0.0)])
    mix.T = Ti
    mix.P = Pi
    mix.equilibrate('HP')
    products = mix.phase(0)
    prodx = dict(zip(products.species_names, products.X))
    fuel = fixDict(fuel)
    ox = fixDict({'N2': 3.76, 'O2': 1})
    inert = fixDict(prodx)
    dfOut = pd.DataFrame(columns=['Xf', 'Xa', 'Xi', 'phi', 'Tad', 'Flammable'])
    Xf = 0.01
    haseverburned = False
    while Xf <= 1.:
        Xa = round(1.0 - Xf, 3)
        burned = False
        while Xa >= 0:
            Xi = abs(round(1.00 - Xf - Xa, 3))
            MMIX = collections.defaultdict(lambda: 0)
            for key in gaslistfull:
                MMIX[key] = Xf * fuel[key] + Xa * ox[key] + Xi * inert[key]
            Tl, Tu = Tblend(MMIX)
            dres = Eqq(MMIX)
            if dres['phi'] > 1:
                if dres['Tad'] > Tu:
                    Flammable = 1
                    burned = True
                    haseverburned = True
                else:
                    Flammable = 0
            else:
                if dres['Tad'] > Tl:
                    Flammable = 1
                    haseverburned = True
                    burned = True
                else:
                    Flammable = 0
            dfOut = dfOut.append(
                {'Xf': Xf, 'Xa': Xa, 'Xi': Xi, 'phi': dres['phi'],
                 'Tad': dres['Tad'], 'Flammable': Flammable},
                ignore_index=True)
            print(Xf, Xa, Xi, Flammable, dres['Tad'])
            if sum(dfOut.iloc[-2::]['Flammable']) == 0.0:
                Xa = round(Xa - 0.1, 1)
            else:
                Xa = round(Xa - 0.01, 3)
        if haseverburned and burned:
            Xf = round(Xf + 0.1, 1)
        else:
            Xf = round(Xf + 0.01, 3)
    return dfOut


def MakePlots(dff, name):
    Xf = np.array(dff.Xf.tolist())
    Xa = np.array(dff.Xa.tolist())
    Xi = np.array(dff.Xi.tolist())
    Tad = np.array(dff.Tad.tolist())
    phi = np.array(dff.phi.tolist())
    phi[phi > 2] = 2
    flm = np.array(dff.Flammable.tolist())
    pio.orca.ensure_server()
    time.sleep(10)
    fgg = ff.create_ternary_contour(np.array([Xf, Xa, Xi]), Tad,
                                    pole_labels=['Fuel', 'Air', 'Inert'],
                                    interp_mode='cartesian', colorscale='Hot',
                                    showscale=True, title=name + 'Tad',
                                    showmarkers=True)
    fgg.write_image(name + "_Tad.png")
    time.sleep(1)
    fgg2 = ff.create_ternary_contour(np.array([Xf, Xa, Xi]), flm,
                                     pole_labels=['Fuel', 'Air', 'Inert'],
                                     interp_mode='cartesian', colorscale='Hot',
                                     title=name + 'Flammability',
                                     ncontours=2)
    fgg2.write_image(name + "_flm.png")
    time.sleep(1)
    fgg3 = ff.create_ternary_contour(np.array([Xf, Xa, Xi]), phi,
                                     pole_labels=['Fuel', 'Air', 'Inert'],
                                     interp_mode='cartesian',
                                     colorscale='Rainbow', ncontours=8,
                                     showscale=True,
                                     title=name + 'Equivalence Ratio')
    fgg3.write_image(name + "_phi.png")
    return fgg, fgg2, fgg3


# dfLFP = doAnalysis(fuelLFP)
# dfLFP.to_csv('fuelLFP.csv')
dfLFP = pd.read_csv('fuelLFP.csv')
MakePlots(dfLFP, 'LFP 2015')

# dfSom = doAnalysis(fuelSom100pct)
# dfSom.to_csv('fuelSom.csv')
# MakePlots(dfSom, 'Somandepalli 100pct')
#
# df10Ah = doAnalysis(fuel10Ah)
# df10Ah.to_csv('fuel10Ah.csv')
# MakePlots(df10Ah, 'UTFRG 10Ah 100pct')
#
# dfCO= doAnalysis({'H2':1})
#
# dfMethane = doAnalysis({'CH4':1})
# dfMethane.to_csv('methane.csv')
# MakePlots(dfMethane, 'Methane')
#
# dfCO = doAnalysis({'CO':1})
# dfCO.to_csv('CO.csv')
# MakePlots(dfCO, 'CO')
#
# dfH2 = doAnalysis({'H2':1})
# dfH2.to_csv('H2.csv')
# MakePlots(dfH2, 'H2')
#
# MakePlots(rw10Ah, rw10Ah, df10Ah)
# MakePlots(rwMethane, rwMethane2, dfMethane)
