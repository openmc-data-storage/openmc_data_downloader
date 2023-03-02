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

from openmc_data_downloader import (
    just_in_time_library_generator,
    LIB_OPTIONS,
    SAB_OPTIONS,
)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l",
        "--libraries",
        choices=LIB_OPTIONS,
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
    parser.add_argument(
        "-s",
        "--sab",
        nargs="*",
        default=[],
        help="The SaB cross sections to download. Options include "
        + " ".join(SAB_OPTIONS),
    )

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

    just_in_time_library_generator(
        libraries=args.libraries,
        isotopes=args.isotopes,
        sab=args.sab,
        elements=args.elements,
        destination=args.destination,
        materials_xml=args.materials_xml,
        particles=args.particles,
        set_OPENMC_CROSS_SECTIONS=False,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
