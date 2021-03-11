

"""
A nuclear data downloading package that facilitates the reproduction of cross
section collections. Use the command line tool or Python API to download the h5
cross sections for just the isotopes / elements that you want. Specify the
prefered nuclear data libraries to use. Automaticallly avoid duplication and
generation of custom cross_section.xml files
"""

import argparse
from pathlib import Path
from typing import Union
from urllib.parse import urlparse
from urllib.request import urlopen

import openmc
import pandas as pd

from endfb_71_nndc import endfb_71_nndc_xs_info

_BLOCK_SIZE = 16384


def download_single_file(
    url: str,
    output_filename: Union[str, Path] = None,
    destination: Union[str, Path] = None
) -> Path:
    """Download file from a URL

    Arguments:
        url: URL from which to download
        destination: Specifies a folder location to save the downloaded file

    Returns
        Name of file written locally
    """

    if output_filename is not None:
        if not isinstance(output_filename, Path):
            output_filename = Path(output_filename)

    if destination is not None:
        if not isinstance(destination, Path):
            destination = Path(destination)

    with urlopen(url) as response:
        # Get file size from header
        file_size = response.length

        if output_filename is None:
            local_path = Path(Path(urlparse(url).path).name)
        else:
            local_path = output_filename

        if destination is not None:
            Path(destination).mkdir(parents=True, exist_ok=True)
            local_path = destination / local_path

        # Check if file already downloaded
        if local_path.is_file():
            if local_path.stat().st_size == file_size:
                print('Skipping {}, already downloaded'.format(local_path))
                return local_path

        # Copy file to disk in chunks
        print('Downloading {}... '.format(local_path), end='')
        with open(local_path, 'wb') as fh:
            while True:
                chunk = response.read(_BLOCK_SIZE)
                if not chunk:
                    break
                fh.write(chunk)
            print('')

    return local_path


def download_data_frame_of_isotopes(dataframe, destination):

    if len(dataframe) == 0:
        print("""\nError. No isotopes matching the required inputs were found.
                \nTry including more library options\n""")

    local_files = []
    for index, row in dataframe.iterrows():
        local_file = download_single_file(
            url=row['url'],
            output_filename=row['local_file'],
            destination=destination
        )
        local_files.append(local_file)

    return local_files


def create_cross_sections_xml(dataframe, destination):

    library = openmc.data.DataLibrary()
    for index, row in dataframe.iterrows():
        library.register_file( Path(destination) / Path(row['local_file']))
    if destination is None:
        library.export_to_xml('cross_sections.xml')
    else:
        if not isinstance(destination, Path):
            destination = Path(destination)
            destination.mkdir(parents=True, exist_ok=True)
        library.export_to_xml(destination / 'cross_sections.xml')

    return library


def identify_isotopes_to_download(libraries, isotopes):

    priority_dict = {}

    for counter, entry in enumerate(libraries):
        priority_dict[entry] = counter+1

    print('Priority of Libraries', priority_dict)

    xs_info = endfb_71_nndc_xs_info  # + ...

    xs_info_df = pd.DataFrame.from_dict(xs_info) 

    is_library = xs_info_df['library'].isin(libraries)
    print('isotopes found matching library requirments', is_library.values.sum())

    if len(isotopes) > 0:
        is_isotope = xs_info_df['isotope'].isin(isotopes)
        print('isotopes found matching isotope requirments', is_isotope.values.sum())

        xs_info_df = xs_info_df[(is_isotope) & (is_library)]
    else:
        xs_info_df = xs_info_df[is_library]

    xs_info_df['priority'] = xs_info_df['library'].map(priority_dict)

    xs_info_df = xs_info_df.sort_values(by=['priority'])

    xs_info_df = xs_info_df.drop_duplicates(['isotope'], keep='first')
    print(len(xs_info_df), 'isotopes found once duplicates have been removed')

    return xs_info_df


def expand_element_to_isotopes(elements):

    isotopes = []
    for element in elements:
        my_mat = openmc.Element(element)
        for nuclide in my_mat.expand(percent=1, percent_type='ao', cross_sections=None):
            isotopes.append(nuclide[0])
    print(isotopes)
    return isotopes


def download_custom_h5_collection(libraries, isotopes, elements, destination):

    print(isotopes)
    if len(elements) > 0:
        isotopes_from_elements = expand_element_to_isotopes(elements)
        isotopes = list(set(isotopes + isotopes_from_elements))

    dataframe = identify_isotopes_to_download(libraries, isotopes)

    download_data_frame_of_isotopes(dataframe, destination)

    create_cross_sections_xml(dataframe, destination)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--libraries', choices=['ENDFB_71_NNDC', 'TENDL-2017',
                        'Jeff-3.3'], nargs='*', help="The nuclear data \
                        libraries to search through when searching for cross \
                        sections. Multiple libaries are acceptable and will \
                        be preferentially utilisd in the order provided"
                        "version.", default=[])   
    parser.add_argument('-i', '--isotopes', nargs='*', default=[], help="The isotopes to \
                        download")   
    parser.add_argument('-e', '--elements', nargs='*', default=[], help="The elements to \
                        download")
    parser.add_argument('-m', '--material_xml', nargs='*', default=[], help="The \
                        filename of the materials.xml file to provide cross \
                        sections for")
    parser.add_argument('-d', '--destination', type=Path, default=None,
                        help='Directory to create new library in')

    args = parser.parse_args()

    download_custom_h5_collection(
        libraries=args.libraries,
        isotopes=args.isotopes,
        elements=args.elements,
        destination=args.destination,
    )
