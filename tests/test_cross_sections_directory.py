from openmc_data_downloader import cross_sections_directory


def test_neutron_isotopes():
    tendl_2019_xs_neutron_info = (
        cross_sections_directory.get_isotopes_or_elements_info_from_xml(
            "neutron",
            "TENDL-2019",
        )
    )
    assert len(tendl_2019_xs_neutron_info) == 630

    nndc_71_neutron_xs_info = (
        cross_sections_directory.get_isotopes_or_elements_info_from_xml(
            "neutron",
            "ENDFB-7.1-NNDC",
        )
    )
    assert len(nndc_71_neutron_xs_info) == 423

    nndc_80_neutron_xs_info = (
        cross_sections_directory.get_isotopes_or_elements_info_from_xml(
            "neutron",
            "ENDFB-8.0-NNDC",
        )
    )
    assert len(nndc_80_neutron_xs_info) == 556

    fendl_31d_neutron_xs_info = (
        cross_sections_directory.get_isotopes_or_elements_info_from_xml(
            "neutron",
            "FENDL-3.1d",
        )
    )
    assert len(fendl_31d_neutron_xs_info) == 180


def test_photon_elements():
    nndc_71_photon_xs_info = (
        cross_sections_directory.get_isotopes_or_elements_info_from_xml(
            "photon",
            "ENDFB-7.1-NNDC",
        )
    )
    assert len(nndc_71_photon_xs_info) == 100

    fendl_31d_photon_xs_info = (
        cross_sections_directory.get_isotopes_or_elements_info_from_xml(
            "photon",
            "FENDL-3.1d",
        )
    )
    assert len(fendl_31d_photon_xs_info) == 59

    nndc_80_photon_xs_info = (
        cross_sections_directory.get_isotopes_or_elements_info_from_xml(
            "photon",
            "ENDFB-8.0-NNDC",
        )
    )
    assert len(nndc_80_photon_xs_info) == 100


def test_sab():
    nndc_71_sab_xs_info = (
        cross_sections_directory.get_isotopes_or_elements_info_from_xml(
            "sab",
            "ENDFB-7.1-NNDC",
        )
    )
    assert len(nndc_71_sab_xs_info) == 20

    nndc_80_sab_xs_info = (
        cross_sections_directory.get_isotopes_or_elements_info_from_xml(
            "sab",
            "ENDFB-8.0-NNDC",
        )
    )
    assert len(nndc_80_sab_xs_info) == 34
