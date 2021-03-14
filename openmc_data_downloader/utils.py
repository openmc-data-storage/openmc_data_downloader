
import math
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Union
from urllib.parse import urlparse
from urllib.request import urlopen
from numpy.lib.function_base import iterable
# from openmc.data.data import isotopes

import pandas as pd

from openmc_data_downloader import NATURAL_ABUNDANCE, LIB_OPTIONS, xs_info

_BLOCK_SIZE = 16384


def set_enviromental_varible(cross_section_xml_path):

    if not isinstance(cross_section_xml_path, Path):
        cross_section_xml_path = Path(cross_section_xml_path)

    if cross_section_xml_path.is_file() is False:
        raise FileNotFoundError(
            '{} was not found, therefore not setting OPENMC_CROSS_SECTIONS '
            'enviromental varible'.format(cross_section_xml_path))

    print('setting OPENMC_CROSS_SECTIONS', str(cross_section_xml_path))
    os.environ["OPENMC_CROSS_SECTIONS"] = str(cross_section_xml_path)


def expand_materials_to_isotopes(materials: list):

    if not isinstance(materials, list):
        materials = [materials]

    if len(materials) > 0:
        isotopes_from_materials = []
        for material in materials:
            for nuc in material.nuclides:
                isotopes_from_materials.append(nuc.name)

        return isotopes_from_materials

    return []


def just_in_time_library_generator(
    libraries: List[str] = [],
    isotopes: List[str] = [],
    elements: List[str] = [],
    destination: Union[str, Path] = None,
    materials_xml: List[Union[str, Path]] = [],
    materials: list = [],
    set_OPENMC_CROSS_SECTIONS: bool = True,
) -> str:

    if len(elements) > 0:
        isotopes_from_elements = expand_elements_to_isotopes(elements)
        isotopes = list(set(isotopes + isotopes_from_elements))

    isotopes_from_material_xml = expand_materials_xml_to_isotopes(materials_xml)
    isotopes = list(set(isotopes + isotopes_from_material_xml))

    isotopes_from_materials = expand_materials_to_isotopes(materials)
    isotopes = list(set(isotopes + isotopes_from_materials))

    dataframe = identify_isotopes_to_download(libraries, isotopes)

    download_data_frame_of_isotopes(dataframe, destination)

    cross_section_xml_path = create_cross_sections_xml(dataframe, destination)

    if set_OPENMC_CROSS_SECTIONS is True:
        set_enviromental_varible(cross_section_xml_path)
    else:
        print('Set your $OPENMC_CROSS_SECTIONS enviromental varible to {} to '
              'use this custom library'.format(cross_section_xml_path))

    return cross_section_xml_path


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
        print('Error. No isotopes matching the required inputs were found. '
              'Try including more library options')

    local_files = []
    for index, row in dataframe.iterrows():
        local_file = download_single_file(
            url=row['url'],
            output_filename=row['local_file'],
            destination=destination
        )
        local_files.append(local_file)

    return local_files


def create_cross_sections_xml(dataframe, destination: Union[str, Path]) -> str:

    try:
        import openmc
    except ImportError:
        print('openmc python package was was found, cross_sections.xml can '
              'not be made.')
        return None

    library = openmc.data.DataLibrary()
    for index, row in dataframe.iterrows():
        if destination is None:
            library.register_file(Path(row['local_file']))
        else:
            library.register_file(Path(destination) / Path(row['local_file']))
    if destination is None:
        library.export_to_xml('cross_sections.xml')
        cross_sections_xml_path = 'cross_sections.xml'
    else:
        if not isinstance(destination, Path):
            destination = Path(destination)
            destination.mkdir(parents=True, exist_ok=True)
        library.export_to_xml(destination / 'cross_sections.xml')
        cross_sections_xml_path = str(destination / 'cross_sections.xml')

    absolute_path = str(Path(cross_sections_xml_path).absolute())
    print(absolute_path, 'written')

    return absolute_path


def identify_isotopes_to_download(libraries: List[str], isotopes: List[str] = []):

    priority_dict = {}

    if isinstance(libraries, str):
        libraries = [libraries]

    if libraries == []:
        raise ValueError('At least one library must be selected, options are', LIB_OPTIONS)

    for counter, entry in enumerate(libraries):
        if entry not in LIB_OPTIONS:
            raise ValueError('The library must be one of the following', LIB_OPTIONS)

        priority_dict[entry] = counter+1

    print('Searching libraries with the following priority', priority_dict)

    # Tried to removed this dict to dataframe conversion out of the function
    # and into the initilisation of the package but this resultied in
    # a SettingwithCopyWarning which can be fized and understood here
    # https://www.dataquest.io/blog/settingwithcopywarning/
    xs_info_df = pd.DataFrame.from_dict(xs_info)

    is_library = xs_info_df['library'].isin(libraries)
    print('Isotopes found matching library requirements', is_library.values.sum())

    if isotopes == []:
        xs_info_df = xs_info_df[is_library]
    else:
        is_isotope = xs_info_df['isotope'].isin(isotopes)
        print('Isotopes found matching isotope requirements', is_isotope.values.sum())

        xs_info_df = xs_info_df[(is_isotope) & (is_library)]

    xs_info_df['priority'] = xs_info_df['library'].map(priority_dict)

    xs_info_df = xs_info_df.sort_values(by=['priority'])

    xs_info_df = xs_info_df.drop_duplicates(['isotope'], keep='first')
    print('Isotopes found matching all requirements', len(xs_info_df))

    return xs_info_df


def expand_elements_to_isotopes(elements):

    isotopes = []
    for element in elements:
        isotopes = isotopes + NATURAL_ABUNDANCE[element]
    return isotopes


def expand_materials_xml_to_isotopes(materials_xml: Union[List[str],str] = 'materials.xml'):

    isotopes = []

    if isinstance(materials_xml, str):
        materials_xml = [materials_xml]

    if materials_xml == []:
        return []

    for material_xml in materials_xml:
        tree = ET.parse(material_xml)
        root = tree.getroot()   

        for elem in root:
            for subelem in elem:
                if 'name' in subelem.attrib.keys():
                    isotopes.append(subelem.attrib['name'])
    return isotopes
