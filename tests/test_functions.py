#!/usr/bin/env python3

__author__ = "Jonathan Shimwell"


import os
import unittest
import time
import pytest

import openmc
import pandas as pd
from openmc_data_downloader import (
    expand_materials_to_isotopes,
    expand_materials_xml_to_isotopes,
    identify_isotopes_to_download,
    identify_sab_to_download,
    expand_elements_to_isotopes,
    expand_materials_xml_to_sab,
    expand_materials_to_sabs,
    download_single_file,
)


def test_expansion_of_elements_with_stable_keyword():
    all_stable_isotopes = expand_elements_to_isotopes("stable")
    assert len(all_stable_isotopes) == 290


def test_expansion_of_elements_with_all_keyword():
    all_stable_isotopes = expand_elements_to_isotopes("all")
    assert len(all_stable_isotopes) == 1233


def test_expansion_of_elements_with_single_element():
    stable_isotopes = expand_elements_to_isotopes("Be")
    assert stable_isotopes == ["Be9"]


def test_expansion_of_elements_with_multiple_element():
    stable_isotopes = expand_elements_to_isotopes(["Be", "Li"])
    assert stable_isotopes == ["Be9", "Li6", "Li7"]


def test_identify_sab_to_download_with_all_keyword():

    filtered_df = identify_sab_to_download(libraries=["ENDFB-7.1-NNDC"], sab=["all"])

    assert len(filtered_df.values) == 20

    filtered_df2 = identify_sab_to_download(libraries=["ENDFB-7.1-NNDC"], sab="all")

    assert len(filtered_df2.values) == 20


def test_identify_sab_to_download_finds_two():

    filtered_df = identify_sab_to_download(
        libraries=["ENDFB-7.1-NNDC"], sab=["c_Be_in_BeO", "c_H_in_H2O"]
    )

    assert len(filtered_df.values) == 2


def test_identify_isotopes_to_download_finds_tendl_neutron():

    filtered_df = identify_isotopes_to_download(
        libraries=["TENDL-2019"], isotopes=["Be9"], particles=["neutron"]
    )
    answer_df = pd.DataFrame.from_dict(
        {
            "isotope": ["Be9"],
            "particle": ["neutron"],
            "library": ["TENDL-2019"],
            "remote_file": ["Be9.h5"],
            "url": [
                "https://github.com/openmc-data-storage/TENDL-2019/raw/main/h5_files/Be9.h5"
            ],
            "element": ["Be"],
            "local_file": ["TENDL-2019_Be9.h5"],
            "priority": [1],
        }
    )
    print(filtered_df)
    assert len(filtered_df.values) == 1
    assert list(filtered_df.keys()) == list(answer_df.keys())
    assert filtered_df.values[0].tolist() == answer_df.values[0].tolist()

    # can't get pandas dataframe comparison to work so resorted to the lists above
    # assert_frame_equal(answer_df, filtered_df)


def test_identify_isotopes_to_download_finds_fendl_photon():

    filtered_df = identify_isotopes_to_download(
        libraries=["FENDL-3.1d"], isotopes=["Be9"], particles=["photon"]
    )
    answer_df = pd.DataFrame.from_dict(
        {
            "isotope": ["Be9"],
            "particle": ["photon"],
            "library": ["FENDL-3.1d"],
            "remote_file": ["Be.h5"],
            "url": [
                "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/photon/Be.h5"
            ],
            "element": ["Be"],
            "local_file": ["FENDL-3.1d_Be.h5"],
            "priority": [1],
        }
    )

    assert len(filtered_df.values) == 1
    assert list(filtered_df.keys()) == list(answer_df.keys())
    assert filtered_df.values[0].tolist() == answer_df.values[0].tolist()


def test_identify_isotopes_to_download_finds_fendl_photon_neutron():

    filtered_df = identify_isotopes_to_download(
        libraries=["FENDL-3.1d"], isotopes=["Be9"], particles=["photon", "neutron"]
    )
    answer_df = pd.DataFrame.from_dict(
        {
            "isotope": ["Be9", "Be9"],
            "particle": ["neutron", "photon"],
            "library": ["FENDL-3.1d", "FENDL-3.1d"],
            "remote_file": ["Be9.h5", "Be.h5"],
            "url": [
                "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/neutron/Be9.h5",
                "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/photon/Be.h5",
            ],
            "element": ["Be", "Be"],
            "local_file": ["FENDL-3.1d_Be9.h5", "FENDL-3.1d_Be.h5"],
            "priority": [1, 1],
        }
    )

    assert len(filtered_df.values) == 2
    assert list(filtered_df.keys()) == list(answer_df.keys())
    assert filtered_df.values[0].tolist() == answer_df.values[0].tolist()
    assert filtered_df.values[1].tolist() == answer_df.values[1].tolist()


def test_identify_isotopes_to_download_finds_fendl_photon_neutron_multi_isotopes():

    filtered_df = identify_isotopes_to_download(
        libraries=["FENDL-3.1d"],
        isotopes=["Fe56", "Fe57"],
        particles=["photon", "neutron"],
    )
    answer_df = pd.DataFrame.from_dict(
        {
            "isotope": ["Fe56", "Fe57", "Fe56"],
            "particle": ["neutron", "neutron", "photon"],
            "library": ["FENDL-3.1d", "FENDL-3.1d", "FENDL-3.1d"],
            "remote_file": ["Fe56.h5", "Fe57.h5", "Fe.h5"],
            "url": [
                "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/neutron/Fe56.h5",
                "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/neutron/Fe57.h5",
                "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/photon/Fe.h5",
            ],
            "element": ["Fe", "Fe", "Fe"],
            "local_file": [
                "FENDL-3.1d_Fe56.h5",
                "FENDL-3.1d_Fe57.h5",
                "FENDL-3.1d_Fe.h5",
            ],
            "priority": [1, 1, 1],
        }
    )

    assert len(filtered_df.values) == 3
    assert list(filtered_df.keys()) == list(answer_df.keys())
    assert filtered_df.values[0].tolist() == answer_df.values[0].tolist()
    assert filtered_df.values[1].tolist() == answer_df.values[1].tolist()
    assert filtered_df.values[2].tolist() == answer_df.values[2].tolist()


def test_identify_isotopes_to_download_all():

    filtered_df = identify_isotopes_to_download(
        libraries=["FENDL-3.1d"], isotopes=["all"], particles=["photon", "neutron"]
    )

    assert len(filtered_df.values) == 239

    filtered_df = identify_isotopes_to_download(
        libraries=["FENDL-3.1d"], isotopes="all", particles=["photon", "neutron"]
    )

    assert len(filtered_df.values) == 239


def test_expand_materials_from_object_list_with_single_mat():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Pu239", 3.7047e-2)
    my_mat.add_nuclide("Pu240", 1.7512e-3)
    my_mat.add_nuclide("Pu241", 1.1674e-4)

    assert expand_materials_to_isotopes([my_mat]) == ["Pu239", "Pu240", "Pu241"]


def test_expand_materials_from_object_with_single_mat():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Pu239", 3.7047e-2)
    my_mat.add_nuclide("Pu240", 1.7512e-3)
    my_mat.add_nuclide("Pu241", 1.1674e-4)

    assert expand_materials_to_isotopes(my_mat) == ["Pu239", "Pu240", "Pu241"]


def test_expand_materials_from_object_list_with_multiple_mat():

    my_mat1 = openmc.Material()
    my_mat1.add_nuclide("Li6", 0.5)
    my_mat1.add_nuclide("Li7", 0.25)

    my_mat2 = openmc.Material()
    my_mat2.add_nuclide("Al27", 0.25)

    assert expand_materials_to_isotopes([my_mat1, my_mat2]) == [
        "Li6",
        "Li7",
        "Al27",
    ]


def test_expand_materials_from_object_list_with_openmc_materials():

    my_mat1 = openmc.Material()
    my_mat1.add_nuclide("Li6", 0.5)
    my_mat1.add_nuclide("Li7", 0.25)

    my_mat2 = openmc.Material()
    my_mat2.add_nuclide("Al27", 0.25)

    mats = openmc.Materials([my_mat1, my_mat2])

    assert expand_materials_to_isotopes(mats) == ["Li6", "Li7", "Al27"]


def test_expand_material_xmls_with_list_input():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Be9", 0.5)
    os.system("rm materials.xml")
    openmc.Materials([my_mat]).export_to_xml()

    assert expand_materials_xml_to_isotopes(["materials.xml"]) == ["Be9"]


def test_expand_material_xmls_with_str_input():

    my_mat = openmc.Material()
    my_mat.add_element("Al", 0.5)
    os.system("rm materials.xml")
    openmc.Materials([my_mat]).export_to_xml()

    assert expand_materials_xml_to_isotopes("materials.xml") == ["Al27"]


def test_expand_material_xmls_with_two_isotopes():

    my_mat = openmc.Material()
    my_mat.add_element("Li", 0.5)
    os.system("rm materials.xml")
    openmc.Materials([my_mat]).export_to_xml()

    assert "Li6" in expand_materials_xml_to_isotopes("materials.xml")
    assert "Li7" in expand_materials_xml_to_isotopes("materials.xml")


def test_expand_material_xmls_with_sab():

    my_mat = openmc.Material()
    my_mat.add_element("Be", 0.5)
    my_mat.add_s_alpha_beta("c_Be_in_BeO")
    os.system("rm materials.xml")
    openmc.Materials([my_mat]).export_to_xml()

    # sab should not be in this list as this is just isotopes
    assert expand_materials_xml_to_isotopes("materials.xml") == ["Be9"]


def test_expand_material_xmls_for_sabs_with_sab():

    my_mat = openmc.Material()
    my_mat.add_element("Be", 0.5)
    my_mat.add_s_alpha_beta("c_Be_in_BeO")
    os.system("rm materials.xml")
    openmc.Materials([my_mat]).export_to_xml()

    assert expand_materials_xml_to_sab("materials.xml") == ["c_Be_in_BeO"]


def test_expand_material_xmls_for_sabs_with_two_sab():

    my_mat = openmc.Material()
    my_mat.add_element("Be", 0.5)
    my_mat.add_s_alpha_beta("c_Be_in_BeO")
    my_mat.add_s_alpha_beta("c_H_in_H2O")
    os.system("rm materials.xml")
    openmc.Materials([my_mat]).export_to_xml()

    assert expand_materials_xml_to_sab("materials.xml") == [
        "c_Be_in_BeO",
        "c_H_in_H2O",
    ]


def test_expand_material_for_sabs_with_two_sab():

    my_mat = openmc.Material()
    my_mat.add_element("Be", 0.5)
    my_mat.add_s_alpha_beta("c_Be_in_BeO")
    my_mat.add_s_alpha_beta("c_H_in_H2O")

    assert expand_materials_to_sabs(my_mat) == ["c_Be_in_BeO", "c_H_in_H2O"]


def test_expand_material_for_sabs_with_sab():

    my_mat = openmc.Material()
    my_mat.add_element("Be", 0.5)
    my_mat.add_s_alpha_beta("c_H_in_H2O")

    assert expand_materials_to_sabs(my_mat) == ["c_H_in_H2O"]


def test_incorrect_material_enpty():
    with pytest.raises(ValueError):
        expand_materials_to_sabs("my_mat")


def test_incorrect_sab_name():
    with pytest.raises(ValueError):
        identify_sab_to_download(libraries=["ENDFB-7.1-NNDC"], sab=["incorrect name"])


def test_incorrect_libraries():
    with pytest.raises(ValueError):
        identify_sab_to_download(libraries=[], sab=["c_Fe56"])


def test_incorrect_library_name_for_sab_identifying():
    with pytest.raises(ValueError):
        identify_sab_to_download(libraries=["incorrect name"], sab=["c_Fe56"])


def test_library_values_single_entry_list():

    isotopes_df = identify_isotopes_to_download(
        libraries="TENDL-2019", isotopes=["Li6", "Al27"], particles=["neutron"]
    )

    assert len(isotopes_df) == 2


def test_emplty_isotopes():
    empty_df = identify_isotopes_to_download(
        libraries=["TENDL-2019"], isotopes=[], particles=["neutron"]
    )
    assert len(empty_df) == 0
    assert isinstance(empty_df, type(pd.DataFrame()))


def test_incorrect_library_values_empty():
    with pytest.raises(ValueError):
        identify_isotopes_to_download(
            libraries=[], isotopes="Li6", particles=["neutron"]
        )


def test_incorrect_library_values_wrong():
    with pytest.raises(ValueError):
        identify_isotopes_to_download(
            libraries=["coucou"], isotopes="Li6", particles=["neutron"]
        )


def test_incorrect_expand_materials_to_isotopes_with_incorrect_args():
    """Checks than an error is raised when incorrect values of materials
    are passed"""

    with pytest.raises(ValueError):
        expand_materials_to_isotopes(1)

    with pytest.raises(ValueError):
        expand_materials_to_isotopes([1, 2, 3])


def test_download_single_file_with_overwrite_speed_up():
    """Checks that downloading with overwrite to False is quicker"""

    current_time = time.time()
    download_single_file(
        url="https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/photon/Fe.h5",
        output_filename="Fe56_new_download.h5",
        overwrite=True,
    )
    time_after_download = time.time()
    time_to_download = time_after_download - current_time

    current_time = time.time()
    download_single_file(
        url="https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/photon/Fe.h5",
        output_filename="Fe56_new_download.h5",
        overwrite=False,
    )
    time_after_download = time.time()
    time_to_not_download = time_after_download - current_time

    assert time_to_not_download < time_to_download
