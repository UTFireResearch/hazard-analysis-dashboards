import sys
sys.path.append('../scripts/')
from H2_model import JetModel
import unittest
import numpy as np

class TestStringMethods(unittest.TestCase):
    ambient_temperature = 300
    ambient_pressure = 101000
    release_temperature = 300
    release_pressure = 4e6
    orifice_diameter = 0.001
    release_angle = 0
    min_concentration = None
    point_along_pathline = None
    contour_of_interest = None
    velocity_if_not_sonic = None

    args = [ambient_temperature, ambient_pressure, release_temperature, release_pressure, orifice_diameter,
                   release_angle, min_concentration, point_along_pathline,
                   contour_of_interest, velocity_if_not_sonic]
    
    Jet = JetModel(*args)
    Jet.run()

    def test_choked(self):
        choked = self.Jet.H2_fluid.choked
        self.assertEqual(choked, True)

    def test_x_distance(self):
        x_separation = np.round(self.Jet.max_x_coords[0],3)
        self.assertEqual(x_separation, 1.514)

    def test_y_distance(self):
        y_separation = np.round(self.Jet.max_y_coords[1],3)
        self.assertEqual(y_separation, 0.061)
    
    def test_pressure(self):
        pressure = np.round(self.Jet.pressure_at_1,3)
        self.assertEqual(pressure, 2085716.601)

if __name__ == '__main__':
    unittest.main()