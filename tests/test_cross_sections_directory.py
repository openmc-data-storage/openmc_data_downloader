
from openmc_data_downloader import cross_sections_directory


def test_neutron_isotopes():
    assert len(cross_sections_directory.tendl_2019_neutron_isotopes) == 630
    assert len(cross_sections_directory.endfb_71_nndc_neutron_isotopes) == 423
    assert len(cross_sections_directory.endfb_71_nndc_photon_elements) == 100
    assert len(cross_sections_directory.fendl_31d_neutron_isotopes) == 180
    assert len(cross_sections_directory.fendl_31d_photon_elements) == 59
#TODO endfb_71_nndc_thermal==20