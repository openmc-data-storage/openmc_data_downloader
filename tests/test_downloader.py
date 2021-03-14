#!/usr/bin/env python3

__author__ = "Jonathan Shimwell"


import os
import unittest
from pathlib import Path

import openmc
from openmc_data_downloader import (expand_materials_to_isotopes,
                                    expand_materials_xml_to_isotopes,
                                    identify_isotopes_to_download,
                                    just_in_time_library_generator)
from openmc_data_downloader.utils import expand_elements_to_isotopes


class test_isotope_finding(unittest.TestCase):

    def test_expand_materials_from_object_list_with_single_mat(self):

        my_mat = openmc.Material()
        my_mat.add_nuclide('Pu239', 3.7047e-2)
        my_mat.add_nuclide('Pu240', 1.7512e-3)
        my_mat.add_nuclide('Pu241', 1.1674e-4)

        assert expand_materials_to_isotopes([my_mat]) == ['Pu239', 'Pu240', 'Pu241']

    def test_expand_materials_from_object_with_single_mat(self):

        my_mat = openmc.Material()
        my_mat.add_nuclide('Pu239', 3.7047e-2)
        my_mat.add_nuclide('Pu240', 1.7512e-3)
        my_mat.add_nuclide('Pu241', 1.1674e-4)

        assert expand_materials_to_isotopes(my_mat) == ['Pu239', 'Pu240', 'Pu241']

    def test_expand_materials_from_object_list_with_multiple_mat(self):

        my_mat1 = openmc.Material()
        my_mat1.add_nuclide('Li6', 0.5)
        my_mat1.add_nuclide('Li7', 0.25)

        my_mat2 = openmc.Material()
        my_mat2.add_nuclide('Al27', 0.25)

        assert expand_materials_to_isotopes([my_mat1, my_mat2]) == ['Li6', 'Li7', 'Al27']

    def test_expand_material_xmls_with_list_input(self):

        my_mat = openmc.Material()
        my_mat.add_nuclide('Be9', 0.5)
        os.system('rm materials.xml')
        openmc.Materials([my_mat]).export_to_xml()

        assert expand_materials_xml_to_isotopes(['materials.xml']) == ['Be9']

    def test_expand_material_xmls_with_str_input(self):

        my_mat = openmc.Material()
        my_mat.add_element('Al', 0.5)
        os.system('rm materials.xml')
        openmc.Materials([my_mat]).export_to_xml()

        assert expand_materials_xml_to_isotopes('materials.xml') == ['Al27']

    def test_library_values_single_entry_list(self):

        isotopes_df = identify_isotopes_to_download(libraries='TENDL_2019', isotopes=['Li6', 'Al27'])

        assert len(isotopes_df) == 2

    def test_incorrect_library_values_empty(self):

        def incorrect_libraries_string():
            identify_isotopes_to_download(libraries=[], isotopes='Li6')

        self.assertRaises(
            ValueError,
            incorrect_libraries_string
        )

    def test_incorrect_library_values_wrong(self):

        def incorrect_libraries_string():
            identify_isotopes_to_download(libraries=['coucou'], isotopes='Li6')

        self.assertRaises(
            ValueError,
            incorrect_libraries_string
        )


class test_command_line_usage(unittest.TestCase):

    def test_single_isotope_download(self):
        os.system('rm *.h5')
        os.system('openmc_data_downloader -l TENDL_2019 -i H1')

        assert Path('TENDL_2019_H1.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 1

    def test_multiple_isotope_download(self):
        os.system('rm *.h5')
        os.system('openmc_data_downloader -l TENDL_2019 -i H1 He4')

        assert Path('TENDL_2019_H1.h5').is_file()
        assert Path('TENDL_2019_He4.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 2

    def test_correct_files_from_command_line_usage_2(self):
        os.system('rm *.h5')
        os.system('openmc_data_downloader -l TENDL_2019 -e F')

        assert Path('TENDL_2019_F19.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 1

    def test_correct_files_from_command_line_usage_3(self):

        os.system('rm *.h5')

        os.system('openmc_data_downloader -l ENDFB_71_NNDC -e Co Y')

        assert Path('ENDFB_71_NNDC_Co59.h5').is_file()
        assert Path('ENDFB_71_NNDC_Y89.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 2

    def test_correct_files_from_command_line_usage_4(self):

        os.system('rm *.h5 materials.xml')

        my_mat = openmc.Material()
        my_mat.add_element('Nb', 0.5)
        my_mat.add_nuclide('Cs133', 0.5)
        os.system('rm materials.xml')
        openmc.Materials([my_mat]).export_to_xml()

        os.system('openmc_data_downloader -l TENDL_2019 -m materials.xml')

        assert expand_materials_xml_to_isotopes(['materials.xml']) == ['Nb93', 'Cs133']

        assert Path('TENDL_2019_Nb93.h5').is_file()
        assert Path('TENDL_2019_Cs133.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 2

    def test_correct_files_from_command_line_usage_5(self):
        """Tests downloading with FENDL"""
        os.system('rm *.h5 materials.xml')

        my_mat = openmc.Material()
        my_mat.add_element('Nb', 0.5)
        os.system('rm materials.xml')
        openmc.Materials([my_mat]).export_to_xml()

        os.system('openmc_data_downloader -l FENDL_31d -m materials.xml')

        assert expand_materials_xml_to_isotopes(['materials.xml']) == ['Nb93']

        assert Path('FENDL_31d_Nb93.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 1

    def test_correct_files_from_command_line_usage_6(self):
        """Tests downloading with FENDL as prioity but without the element in
        FENDL"""

        os.system('rm *.h5')

        os.system('openmc_data_downloader -l FENDL_31d TENDL_2019 -e Pr')

        assert expand_elements_to_isotopes(['Pr']) == ['Pr141']

        assert Path('TENDL_2019_Pr141.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 1


class test_usage_with_openmc_python_api(unittest.TestCase):

    def test_simulation_with_destination(self):

        os .system('rm *.h5')
        os .system('rm my_custom_nuclear_data_dir/*.h5')

        # Define material
        my_mat = openmc.openmc.Material()
        my_mat.add_nuclide('Pu239', 3.7047e-2)
        my_mat.add_nuclide('Pu240', 1.7512e-3)
        my_mat.add_nuclide('As75', 1.3752e-3)
        openmc.openmc.Materials([my_mat]).export_to_xml()

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

        just_in_time_library_generator(
            destination='my_custom_nuclear_data_dir',
            libraries=['TENDL_2019'],
            materials=my_mat,
            set_OPENMC_CROSS_SECTIONS=True
        )

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('my_custom_nuclear_data_dir/TENDL_2019_Pu239.h5').is_file()
        assert Path('my_custom_nuclear_data_dir/TENDL_2019_Pu240.h5').is_file()
        assert Path('my_custom_nuclear_data_dir/TENDL_2019_As75.h5').is_file()
        assert Path('statepoint.2.h5').is_file()
        assert len(list(Path('my_custom_nuclear_data_dir').glob('*.h5'))) == 3

    def test_simulation_with_single_mat(self):

        os .system('rm *.h5')

        # Define material
        my_mat = openmc.openmc.Material()
        my_mat.add_nuclide('Pu239', 3.7047e-2)
        my_mat.add_nuclide('Pu240', 1.7512e-3)
        my_mat.add_nuclide('As75', 1.3752e-3)
        openmc.openmc.Materials([my_mat]).export_to_xml()

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

        just_in_time_library_generator(libraries=['TENDL_2019'], materials=my_mat, set_OPENMC_CROSS_SECTIONS=True)

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('TENDL_2019_Pu239.h5').is_file()
        assert Path('TENDL_2019_Pu240.h5').is_file()
        assert Path('TENDL_2019_As75.h5').is_file()
        assert Path('statepoint.2.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 5  # summary and statepoint

    def test_simulation_with_single_mat_list(self):

        os .system('rm *.h5')

        # Define material
        my_mat = openmc.openmc.Material()
        my_mat.add_nuclide('Pu239', 3.7047e-2)
        my_mat.add_nuclide('Pu240', 1.7512e-3)
        my_mat.add_nuclide('As75', 1.3752e-3)
        openmc.openmc.Materials([my_mat]).export_to_xml()

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
        assert Path('TENDL_2019_As75.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 5  # summary and statepoint
        assert Path('statepoint.2.h5').is_file()

    def test_simulation_with_multi_mat_list(self):

        os .system('rm *.h5')

        # Define material
        my_mat1 = openmc.openmc.Material()
        my_mat1.add_nuclide('Pu239', 3.7047e-2)
        my_mat1.add_nuclide('Pu240', 1.7512e-3)

        my_mat2 = openmc.openmc.Material()
        my_mat2.add_element('As', 1.3752e-3)
        openmc.openmc.Materials([my_mat1, my_mat2]).export_to_xml()

        # Create a sphere of my_mat
        surf1 = openmc.Sphere(r=1)
        surf2 = openmc.Sphere(r=6, boundary_type='vacuum')
        main_cell = openmc.Cell(fill=my_mat1, region=-surf1)
        outer_cell = openmc.Cell(fill=my_mat2, region=+surf1 & -surf2)
        universe = openmc.Universe(cells=[main_cell, outer_cell])
        openmc.Geometry(universe).export_to_xml()

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

        just_in_time_library_generator(libraries=['TENDL_2019'], materials=[my_mat1, my_mat2], set_OPENMC_CROSS_SECTIONS=True)

        os.system('echo $OPENMC_CROSS_SECTIONS')
        openmc.run()

        assert Path('TENDL_2019_Pu239.h5').is_file()
        assert Path('TENDL_2019_Pu240.h5').is_file()
        assert Path('TENDL_2019_As75.h5').is_file()
        assert Path('statepoint.2.h5').is_file()
        assert len(list(Path('.').glob('*.h5'))) == 5  # summary and statepoint
