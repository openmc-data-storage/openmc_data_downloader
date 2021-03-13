#!/usr/bin/env python3

__author__ = "Jonathan Shimwell"


import os
import unittest
from pathlib import Path

import openmc
from openmc_data_downloader import just_in_time_library_generator


class test_usage_withOpenmc_python_api(unittest.TestCase):

    def test_is(self):
    # def test_isotope_download_and_setting_openmc_cross_sections_for_simulation(self):

        # os .system('rm *.h5')

        # Define material
        my_mat = openmc.Material()
        my_mat.add_nuclide('Pu239', 3.7047e-2)
        my_mat.add_nuclide('Pu240', 1.7512e-3)
        my_mat.add_nuclide('Pu241', 1.1674e-4)
        my_mat.add_element('As', 1.3752e-3)
        openmc.Materials([my_mat]).export_to_xml()

        # Create a sphere of my_mat
        surf = openmc.Sphere(r=6.3849, boundary_type='vacuum')
        main_cell = openmc.Cell(fill=my_mat, region=-surf)
        openmc.Geometry([main_cell]).export_to_xml()

        # Define settings for the simulation
        settings = openmc.Settings()
        settings.particles = 10
        settings.batches = 2
        settings.inactive = 0
        center = (0., 0., 0.)
        settings.source = openmc.Source(space=openmc.stats.Point(center))
        settings.export_to_xml()

        # this clears the enviromental varible just to be sure that current system settings are not being used
        os.environ["OPENMC_CROSS_SECTIONS"] = ''

        just_in_time_library_generator(libraries=['TENDL_2019'], materials=[my_mat], set_OPENMC_CROSS_SECTIONS=True)

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('TENDL_2019_Pu239.h5').is_file()
        assert Path('TENDL_2019_Pu240.h5').is_file()
        assert Path('TENDL_2019_Pu241.h5').is_file()
        assert Path('TENDL_2019_As75.h5').is_file()
        assert Path('statepoint.2.h5').is_file()
