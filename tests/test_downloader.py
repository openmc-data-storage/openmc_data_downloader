#!/usr/bin/env python3

__author__ = "Jonathan Shimwell"


import os
import unittest

from openmc import Material, Materials
from openmc_data_downloader import (expand_materials_to_isotopes,
                                    expand_materials_xml_to_isotopes,
                                    identify_isotopes_to_download)


class test_command_line_usage(unittest.TestCase):

    def test_expand_materials_from_object_list_with_single_mat(self):

        my_mat = Material()
        my_mat.add_nuclide('Pu239', 3.7047e-2)
        my_mat.add_nuclide('Pu240', 1.7512e-3)
        my_mat.add_nuclide('Pu241', 1.1674e-4)

        assert expand_materials_to_isotopes([my_mat]) == ['Pu239', 'Pu240', 'Pu241']

    def test_expand_materials_from_object_list_with_multiple_mat(self):

        my_mat1 = Material()
        my_mat1.add_nuclide('Li6', 0.5)
        my_mat1.add_nuclide('Li7', 0.25)

        my_mat2 = Material()
        my_mat2.add_nuclide('Al27', 0.25)

        assert expand_materials_to_isotopes([my_mat1, my_mat2]) == ['Li6', 'Li7', 'Al27']

    def test_expand_material_xmls_with_list_input(self):

        my_mat = Material()
        my_mat.add_nuclide('Be9', 0.5)
        os.system('rm materials.xml')
        Materials([my_mat]).export_to_xml()

        assert expand_materials_xml_to_isotopes(['materials.xml']) == ['Be9']

    def test_expand_material_xmls_with_str_input(self):

        my_mat = Material()
        my_mat.add_element('Al', 0.5)
        os.system('rm materials.xml')
        Materials([my_mat]).export_to_xml()

        assert expand_materials_xml_to_isotopes('materials.xml') == ['Al27']

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
