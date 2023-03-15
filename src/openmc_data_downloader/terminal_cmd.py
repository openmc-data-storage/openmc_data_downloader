#!/usr/bin/python

"""
A nuclear data downloading package that facilitates the reproduction of cross
section collections. Use the command line tool or Python API to download the h5
cross sections for just the isotopes / elements that you want. Specify the
preferred nuclear data libraries to use. Automatically avoid duplication and
generation of custom cross_section.xml files
"""

import argparse
from pathlib import Path
import openmc_data_downloader
import openmc


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l",
        "--libraries",
        choices=openmc_data_downloader.LIB_OPTIONS,
        nargs="*",
        help="The nuclear data libraries to search through when searching for \
        cross sections. Multiple libaries are acceptable and will be \
        preferentially utilized in the order provided",
        default=[],
        required=True,
    )
    parser.add_argument(
        "-i",
        "--isotopes",
        nargs="*",
        default=[],
        help="The isotope or isotopes to download, name of isotope e.g. 'Al27' or keyword 'all' or 'stable'",
    )
    # parser.add_argument(
    #     "-s",
    #     "--sab",
    #     nargs="*",
    #     default=[],
    #     help="The SaB cross sections to download. Options include "
    #     + " ".join(SAB_OPTIONS),
    # )

    parser.add_argument(
        "-e",
        "--elements",
        nargs="*",
        default=[],
        help="The element or elements to download, name of element e.g. 'Al' or keyword 'all' or 'stable'",
    )
    parser.add_argument(
        "-p",
        "--particles",
        nargs="*",
        default=["neutron"],
        choices=["neutron", "photon"],
        help="The particle to download",
    )
    parser.add_argument(
        "-m",
        "--materials_xml",
        nargs="*",
        default=[],
        help="The filename of the materials.xml file to \
            provide cross sections for",
    )
    parser.add_argument(
        "-d",
        "--destination",
        type=Path,
        default=None,
        help="Directory to create new library in",
    )

    parser.add_argument(
        "--overwrite", action="store_true", help="Exiting files will be overwritten"
    )

    parser.add_argument(
        "--no-overwrite",
        action="store_false",
        help="Exiting files will not be overwritten",
    )

    parser.set_defaults(overwrite=False)
    args = parser.parse_args()

    if args.materials_xml:
        for material_xml in args.materials_xml:
            mats = openmc.Materials.from_xml(material_xml)
            mats.download_cross_section_data(
                libraries=args.libraries,
                destination=args.destination,
                particles=args.particles,
                set_OPENMC_CROSS_SECTIONS=False,
                overwrite=args.overwrite,
            )

    mat = openmc.Material()
    for isotope in args.isotopes:
        mat.add_nuclide(isotope, 1)
    for element in args.elements:
        mat.add_element(element, 1)

    mats = openmc.Materials([mat])
    print(mats)
    mats.download_cross_section_data(
        libraries=args.libraries,
        destination=args.destination,
        particles=args.particles,
        set_OPENMC_CROSS_SECTIONS=False,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
