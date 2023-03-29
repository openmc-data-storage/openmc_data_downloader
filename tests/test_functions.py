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
    identify_isotopes_to_download,
    identify_sabs_to_download,
    expand_materials_to_sabs,
    download_single_file,
)


def test_identify_isotopes_to_download_finds_tendl_neutron():
    filtered_df = identify_isotopes_to_download(
        libraries=["TENDL-2019"], isotopes=["Be9"]
    )
    answer_df = pd.DataFrame.from_dict(
        {
            "library": ["TENDL-2019"],
            "remote_file": ["Be9.h5"],
            "url": [
                "https://github.com/openmc-data-storage/TENDL-2019/raw/main/h5_files/Be9.h5"
            ],
            "local_file": ["TENDL-2019_Be9.h5"],
            "particle": ["neutron"],
            "isotope": ["Be9"],
            "element": ["Be"],
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
        libraries=["FENDL-3.1d"], isotopes=["Be9"]
    )
    answer_df = pd.DataFrame.from_dict(
        {
            "library": ["FENDL-3.1d"],
            "remote_file": ["Be9.h5"],
            "url": [
                "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/neutron/Be9.h5"
            ],
            "local_file": ["FENDL-3.1d_Be9.h5"],
            "particle": ["neutron"],
            "isotope": ["Be9"],
            "element": ["Be"],
            "priority": [1],
        }
    )

    assert len(filtered_df.values) == 1
    assert list(filtered_df.keys()) == list(answer_df.keys())
    assert filtered_df.values[0].tolist() == answer_df.values[0].tolist()


def test_identify_isotopes_to_download_finds_fendl_photon_neutron():
    filtered_df = identify_isotopes_to_download(
        libraries=["FENDL-3.1d"], isotopes=["Be9"]
    )
    answer_df = pd.DataFrame.from_dict(
        {
            "library": ["FENDL-3.1d"],
            "remote_file": ["Be9.h5"],
            "url": [
                "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/neutron/Be9.h5",
            ],
            "local_file": ["FENDL-3.1d_Be9.h5"],
            "particle": ["neutron"],
            "isotope": ["Be9"],
            "element": ["Be"],
            "priority": [1],
        }
    )

    assert len(filtered_df.values) == 1
    assert list(filtered_df.keys()) == list(answer_df.keys())
    assert filtered_df.values[0].tolist() == answer_df.values[0].tolist()


def test_identify_isotopes_to_download_finds_fendl_photon_neutron_multi_isotopes():
    filtered_df = identify_isotopes_to_download(
        libraries=["FENDL-3.1d"],
        isotopes=["Fe56", "Fe57"],
    )
    answer_df = pd.DataFrame.from_dict(
        {
            "library": ["FENDL-3.1d", "FENDL-3.1d"],
            "remote_file": ["Fe56.h5", "Fe57.h5"],
            "url": [
                "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/neutron/Fe56.h5",
                "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/neutron/Fe57.h5",
            ],
            "local_file": [
                "FENDL-3.1d_Fe56.h5",
                "FENDL-3.1d_Fe57.h5",
            ],
            "particle": ["neutron", "neutron"],
            "isotope": ["Fe56", "Fe57"],
            "element": ["Fe", "Fe"],
            "priority": [1, 1],
        }
    )

    assert len(filtered_df.values) == 2
    assert list(filtered_df.keys()) == list(answer_df.keys())
    assert filtered_df.values[0].tolist() == answer_df.values[0].tolist()
    assert filtered_df.values[1].tolist() == answer_df.values[1].tolist()


def test_identify_isotopes_to_download_all():
    filtered_df = identify_isotopes_to_download(
        libraries=["FENDL-3.1d"], isotopes=["all"]
    )

    assert len(filtered_df.values) == 180

    filtered_df = identify_isotopes_to_download(
        libraries=["FENDL-3.1d"], isotopes="all"
    )

    assert len(filtered_df.values) == 180


def test_expand_materials_from_object_list_with_single_mat():
    my_mat = openmc.Material()
    my_mat.add_nuclide("Pu239", 3.7047e-2)
    my_mat.add_nuclide("Pu240", 1.7512e-3)
    my_mat.add_nuclide("Pu241", 1.1674e-4)

    assert expand_materials_to_isotopes(openmc.Materials([my_mat])) == [
        "Pu239",
        "Pu240",
        "Pu241",
    ]


def test_expand_materials_from_object_with_single_mat():
    my_mat = openmc.Material()
    my_mat.add_nuclide("Pu239", 3.7047e-2)
    my_mat.add_nuclide("Pu240", 1.7512e-3)
    my_mat.add_nuclide("Pu241", 1.1674e-4)

    assert expand_materials_to_isotopes(openmc.Materials([my_mat])) == [
        "Pu239",
        "Pu240",
        "Pu241",
    ]


def test_expand_materials_from_object_list_with_multiple_mat():
    my_mat1 = openmc.Material()
    my_mat1.add_nuclide("Li6", 0.5)
    my_mat1.add_nuclide("Li7", 0.25)

    my_mat2 = openmc.Material()
    my_mat2.add_nuclide("Al27", 0.25)

    assert expand_materials_to_isotopes(openmc.Materials([my_mat1, my_mat2])) == [
        "Al27",
        "Li6",
        "Li7",
    ]


def test_expand_materials_from_object_list_with_openmc_materials():
    my_mat1 = openmc.Material()
    my_mat1.add_nuclide("Li6", 0.5)
    my_mat1.add_nuclide("Li7", 0.25)

    my_mat2 = openmc.Material()
    my_mat2.add_nuclide("Al27", 0.25)

    mats = openmc.Materials([my_mat1, my_mat2])

    assert expand_materials_to_isotopes(mats) == ["Al27", "Li6", "Li7"]


def test_expand_material_xmls_for_sabs_with_sab():
    my_mat = openmc.Material()
    my_mat.add_element("Be", 0.5)
    my_mat.add_s_alpha_beta("c_Be_in_BeO")
    my_mats = openmc.Materials([my_mat])

    assert expand_materials_to_sabs(my_mats) == ["c_Be_in_BeO"]


def test_expand_material_xmls_for_sabs_with_two_sab():
    my_mat = openmc.Material()
    my_mat.add_element("Be", 0.5)
    my_mat.add_s_alpha_beta("c_Be_in_BeO")
    my_mat.add_s_alpha_beta("c_H_in_H2O")
    my_mats = openmc.Materials([my_mat])

    assert expand_materials_to_sabs(my_mats) == [
        "c_Be_in_BeO",
        "c_H_in_H2O",
    ]


def test_expand_material_for_sabs_with_two_sab():
    my_mat = openmc.Material()
    my_mat.add_element("Be", 0.5)
    my_mat.add_s_alpha_beta("c_Be_in_BeO")
    my_mat.add_s_alpha_beta("c_H_in_H2O")
    my_mats = openmc.Materials([my_mat])
    assert expand_materials_to_sabs(my_mats) == ["c_Be_in_BeO", "c_H_in_H2O"]


def test_expand_material_for_sabs_with_sab():
    my_mat = openmc.Material()
    my_mat.add_element("Be", 0.5)
    my_mat.add_s_alpha_beta("c_H_in_H2O")
    my_mats = openmc.Materials([my_mat])

    assert expand_materials_to_sabs(my_mats) == ["c_H_in_H2O"]


def test_incorrect_material_enpty():
    with pytest.raises(ValueError):
        expand_materials_to_sabs("my_mat")


def test_incorrect_sab_name():
    with pytest.raises(ValueError):
        identify_sabs_to_download(libraries=["ENDFB-7.1-NNDC"], sabs=["incorrect name"])


def test_incorrect_libraries():
    with pytest.raises(ValueError):
        identify_sabs_to_download(libraries=[], sabs=["c_Fe56"])


def test_incorrect_library_name_for_sab_identifying():
    with pytest.raises(ValueError):
        identify_sabs_to_download(libraries=["incorrect name"], sabs=["c_Fe56"])


def test_library_values_single_entry_list():
    isotopes_df = identify_isotopes_to_download(
        libraries=["TENDL-2019"], isotopes=["Al27", "Li6"]
    )

    assert len(isotopes_df) == 2


def test_emplty_isotopes():
    empty_df = identify_isotopes_to_download(libraries=["TENDL-2019"], isotopes=[])
    assert len(empty_df) == 0
    assert isinstance(empty_df, type(pd.DataFrame()))


def test_incorrect_library_values_empty():
    with pytest.raises(ValueError):
        identify_isotopes_to_download(libraries=[], isotopes="Li6")


def test_incorrect_library_values_wrong():
    with pytest.raises(ValueError):
        identify_isotopes_to_download(libraries=["coucou"], isotopes="Li6")


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
