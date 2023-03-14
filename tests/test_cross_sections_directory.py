from openmc_data_downloader import cross_sections_directory


def test_neutron_isotopes():
    tendl_2019_xs_neutron_info = cross_sections_directory.get_isotopes_or_elements_info_from_xml(
        "tendl_2019_cross_sections.xml",
        "neutron",
        "https://github.com/openmc-data-storage/TENDL-2019/raw/main/h5_files/",
        "TENDL-2019",
    )
    assert len(tendl_2019_xs_neutron_info) == 630

    nndc_71_neutron_xs_info = cross_sections_directory.get_isotopes_or_elements_info_from_xml(
        "nndc_7.1_cross_sections.xml",
        "neutron",
        "https://github.com/openmc-data-storage/ENDF-B-VII.1-NNDC/raw/main/h5_files/neutron/",
        "ENDFB-7.1-NNDC",
    )
    assert len(nndc_71_neutron_xs_info) == 423

    nndc_80_neutron_xs_info = cross_sections_directory.get_isotopes_or_elements_info_from_xml(
        "nndc_8.0_cross_sections.xml",
        "neutron",
        "https://github.com/openmc-data-storage/ENDF-B-VIII.0-NNDC/raw/main/h5_files/neutron/",
        "ENDFB-8.0-NNDC",
    )
    assert len(nndc_80_neutron_xs_info) == 556

    fendl_31d_neutron_xs_info = cross_sections_directory.get_isotopes_or_elements_info_from_xml(
        "fendl_3.1d_cross_sections.xml",
        "neutron",
        "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/neutron/",
        "FENDL-3.1d",
    )
    assert len(fendl_31d_neutron_xs_info) == 180


def test_photon_elements():
    nndc_71_photon_xs_info = cross_sections_directory.get_isotopes_or_elements_info_from_xml(
        "nndc_7.1_cross_sections.xml",
        "photon",
        "https://github.com/openmc-data-storage/ENDF-B-VII.1-NNDC/raw/main/h5_files/photon/",
        "ENDFB-7.1-NNDC",
    )
    assert len(nndc_71_photon_xs_info) == 100

    fendl_31d_photon_xs_info = cross_sections_directory.get_isotopes_or_elements_info_from_xml(
        "fendl_3.1d_cross_sections.xml",
        "photon",
        "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/photon/",
        "FENDL-3.1d",
    )
    assert len(fendl_31d_photon_xs_info) == 59

    nndc_80_photon_xs_info = cross_sections_directory.get_isotopes_or_elements_info_from_xml(
        "nndc_8.0_cross_sections.xml",
        "photon",
        "https://github.com/openmc-data-storage/ENDF-B-VIII.0-NNDC/raw/main/h5_files/photon/",
        "ENDFB-8.0-NNDC",
    )
    assert len(nndc_80_photon_xs_info) == 100


# TODO endfb_71_nndc_thermal==20
