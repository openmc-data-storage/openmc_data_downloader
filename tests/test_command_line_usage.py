#!/usr/bin/env python3

__author__ = "Jonathan Shimwell"


import os
import time
from pathlib import Path

import openmc
import openmc_data_downloader

import pytest

# def test_single_isotope_download_endf_71_wmp():
#     os.system("rm *.h5")
#     os.system("openmc_data_downloader -l ENDFB-7.1-WMP -i H1")

#     assert Path("ENDFB-7.1-WMP_H1.h5").is_file()
#     assert len(list(Path(".").glob("*.h5"))) == 1


def test_single_isotope_download_tendl_2019():
    os.system("rm *.h5")
    os.system("openmc_data_downloader -l TENDL-2019 -i H1")

    assert Path("TENDL-2019_H1.h5").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 1


def test_multiple_isotope_download():
    os.system("rm *.h5")
    os.system("openmc_data_downloader -l TENDL-2019 -i H1 He4")

    assert Path("TENDL-2019_H1.h5").is_file()
    assert Path("TENDL-2019_He4.h5").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 2


def test_correct_files_from_command_line_usage_2():
    os.system("rm *.h5")
    os.system("openmc_data_downloader -l TENDL-2019 -e F")

    assert Path("TENDL-2019_F19.h5").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 1


@pytest.mark.parametrize("lib", ("ENDFB-7.1", "ENDFB-8.0", "ENDFB-8.1"))
def test_correct_files_from_command_line_usage_3(lib):
    os.system("rm *.h5")

    os.system(f"openmc_data_downloader -l {lib}-NNDC -e Co Y")

    assert Path(f"{lib}-NNDC_Co59.h5").is_file()
    assert Path(f"{lib}-NNDC_Y89.h5").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 2

    Path(f"{lib}-NNDC_Co59.h5").unlink()
    Path(f"{lib}-NNDC_Y89.h5").unlink()


def test_correct_files_from_command_line_usage_4():
    os.system("rm *.h5 materials.xml")

    my_mat = openmc.Material()
    my_mat.add_element("Nb", 0.5)
    my_mat.add_nuclide("Cs133", 0.5)
    os.system("rm materials.xml")
    openmc.Materials([my_mat]).export_to_xml()

    os.system("openmc_data_downloader -l TENDL-2019 -m materials.xml")

    assert Path("TENDL-2019_Nb93.h5").is_file()
    assert Path("TENDL-2019_Cs133.h5").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 2


def test_correct_files_from_command_line_usage_5():
    """Tests downloading with FENDL"""
    os.system("rm *.h5 materials.xml")

    my_mat = openmc.Material()
    my_mat.add_element("Nb", 0.5)
    os.system("rm materials.xml")
    openmc.Materials([my_mat]).export_to_xml()

    os.system("openmc_data_downloader -l FENDL-3.1d -m materials.xml -p neutron")

    assert Path("FENDL-3.1d_Nb93.h5").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 1


def test_correct_files_from_command_line_usage_6():
    """Tests downloading with FENDL as priority but without the element in
    FENDL"""

    os.system("rm *.h5")

    os.system("openmc_data_downloader -l FENDL-3.1d TENDL-2019 -e Pr")

    assert Path("TENDL-2019_Pr141.h5").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 1


@pytest.mark.parametrize("lib", ("ENDFB-7.1", "ENDFB-8.0", "ENDFB-8.1"))
def test_photon_download_of_isotope_nndc(lib):
    """Tests downloading with NNDC photon data and checks it exists"""

    os.system("rm *.h5")

    os.system(f"openmc_data_downloader -l {lib}-NNDC -i He4 -p photon")

    assert Path(f"{lib}-NNDC_He.h5").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 1

    Path(f"{lib}-NNDC_He.h5").unlink()


def test_photon_download_of_isotope_fendl():
    """Tests downloading with FENDL photon data and checks it exists"""

    os.system("rm *.h5")

    os.system("openmc_data_downloader -l FENDL-3.1d -i He4 -p photon")

    assert Path("FENDL-3.1d_He.h5").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 1


def test_neutron_and_photon_download_of_isotope_fendl():
    """Tests downloading with FENDL photon data and checks it exists"""

    os.system("rm *.h5")

    os.system("openmc_data_downloader -l FENDL-3.1d -i He4 -p photon neutron")

    assert Path("FENDL-3.1d_He.h5").is_file()
    assert Path("FENDL-3.1d_He4.h5").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 2


@pytest.mark.parametrize(
    "lib",
    (
        "ENDFB-7.1",
        pytest.param(
            "ENDFB-8.0", marks=pytest.mark.xfail(reason="SABs not stored in repo")
        ),
        "ENDFB-8.1",
    ),
)
def test_sab_download_with_endf(lib):
    """Tests downloading with FENDL photon data and checks it exists"""

    os.system("rm *.h5")

    os.system(f"openmc_data_downloader -l {lib}-NNDC TENDL-2019 -e Be O -s c_Be_in_BeO")

    assert Path(f"{lib}-NNDC_Be9.h5").is_file()
    assert Path(f"{lib}-NNDC_O16.h5").is_file()
    assert Path(f"{lib}-NNDC_O17.h5").is_file()
    if lib == "ENDFB-7.1":
        assert Path("TENDL-2019_O18.h5").is_file()
    else:
        assert Path(f"{lib}-NNDC_O18.h5").is_file()
    assert Path(f"{lib}-NNDC_c_Be_in_BeO.h5").is_file()
    assert Path("materials.xml").is_file()
    assert len(list(Path(".").glob("*.h5"))) == 5


def test_download_single_file_with_overwrite_speed_up():
    """Checks that downloading with overwrite to False is quicker"""

    current_time = time.time()
    os.system("openmc_data_downloader -l ENDFB-7.1-NNDC TENDL-2019 -e Be --overwrite")
    time_after_download = time.time()
    time_to_download = time_after_download - current_time

    current_time = time.time()
    os.system(
        "openmc_data_downloader -l ENDFB-7.1-NNDC TENDL-2019 -e Be --no-overwrite",
    )
    time_after_download = time.time()
    time_to_not_download = time_after_download - current_time

    assert time_to_not_download < time_to_download
