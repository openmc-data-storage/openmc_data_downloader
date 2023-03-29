import os
import xml.etree.ElementTree as ET
from pathlib import Path
import typing
from typing import List, Optional, Union
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import HTTPError
import pandas as pd
from retry import retry
import openmc


from openmc_data_downloader import (
    ALL_ISOTOPE_OPTIONS,
    STABLE_ISOTOPE_OPTIONS,
    ALL_ELEMENT_OPTIONS,
    STABLE_ELEMENT_OPTIONS,
    LIB_OPTIONS,
    PARTICLE_OPTIONS,
    neutron_xs_info,
    photon_xs_info,
    sab_xs_info,
    SAB_OPTIONS,
)

_BLOCK_SIZE = 16384


def set_environmental_variable(cross_section_xml_path: Union[Path, str]) -> None:
    if not isinstance(cross_section_xml_path, Path):
        cross_section_xml_path = Path(cross_section_xml_path)

    if cross_section_xml_path.is_file() is False:
        raise FileNotFoundError(
            f"{cross_section_xml_path} was not found, therefore not setting "
            "OPENMC_CROSS_SECTIONS environmental variable"
        )

    print(f"setting OPENMC_CROSS_SECTIONS to {str(cross_section_xml_path)}")
    os.environ["OPENMC_CROSS_SECTIONS"] = str(cross_section_xml_path)
    # openmc.config['cross_sections'] = cross_section_xml_path


def expand_materials_to_isotopes(materials: openmc.Materials):
    if not isinstance(materials, openmc.Materials):
        raise ValueError("materials argument must be an openmc.Materials() object")
    if len(materials) == 0:
        raise ValueError(
            "There are no openmc.Material() entries within the openmc.Materials() object"
        )

    isotopes_from_materials = []
    for material in materials:
        for nuc in material.nuclides:
            isotopes_from_materials.append(nuc.name)

    return sorted(list(set(isotopes_from_materials)))


def expand_materials_to_sabs(materials: openmc.Materials):
    if not isinstance(materials, openmc.Materials):
        raise ValueError("materials argument must be an openmc.Materials() object")
    if len(materials) == 0:
        raise ValueError(
            "There are no openmc.Material() entries within the openmc.Materials() object"
        )

    sabs_from_materials = []
    for material in materials:
        for sab in material._sab:
            sabs_from_materials.append(sab[0])

    return sorted(list(set(sabs_from_materials)))


def expand_materials_to_elements(materials: openmc.Materials):
    if not isinstance(materials, openmc.Materials):
        raise ValueError("materials argument must be an openmc.Materials() object")
    if len(materials) == 0:
        raise ValueError(
            "There are no openmc.Material() entries within the openmc.Materials() object"
        )

    elements_from_materials = []
    for material in materials:
        elements = material.get_elements()
        elements_from_materials = elements_from_materials + elements

    return list(set(elements_from_materials))


def download_cross_section_data(
    self,
    libraries: typing.Iterable[str] = (
        "TENDL-2019",
        "ENDFB-7.1-NNDC",
        "ENDFB-8.0-NNDC",
        "FENDL-3.1d",
    ),
    destination: Union[str, Path] = None,
    particles: Optional[typing.Iterable[str]] = ("neutron", "photon"),
    set_OPENMC_CROSS_SECTIONS: bool = True,
    overwrite: bool = False,
) -> str:
    """ """

    for entry in particles:
        if entry not in PARTICLE_OPTIONS:
            raise ValueError(
                f"The particle must be one of the following {PARTICLE_OPTIONS}. Not {entry}"
            )

    dataframe = pd.DataFrame()

    if "neutron" in particles:
        isotopes = expand_materials_to_isotopes(self)
        # filters the large dataframe of all isotopes into just the ones you want
        dataframe_isotopes_xs = identify_isotopes_to_download(
            libraries=libraries,
            isotopes=isotopes,
        )
        dataframe = pd.concat([dataframe, dataframe_isotopes_xs])

    if "photon" in particles:
        elements = expand_materials_to_elements(self)
        dataframe_elements_xs = identify_elements_to_download(
            libraries=libraries,
            elements=elements,
        )
        dataframe = pd.concat([dataframe, dataframe_elements_xs])

    sabs = expand_materials_to_sabs(self)
    if len(sabs) > 0:
        dataframe_sabs_xs = identify_sabs_to_download(
            libraries=libraries,
            sabs=sabs,
        )
        dataframe = pd.concat([dataframe, dataframe_sabs_xs])
        print("dataframe_sabs_xs", dataframe_sabs_xs)

    print(dataframe)

    download_data_frame_of(
        dataframe=dataframe, destination=destination, overwrite=overwrite
    )

    cross_section_xml_path = create_cross_sections_xml(dataframe, destination)

    if set_OPENMC_CROSS_SECTIONS is True:
        self.cross_sections = cross_section_xml_path
        # making the cross section xml requires openmc and returns None if
        # openmc is not found.
        if cross_section_xml_path is not None:
            set_environmental_variable(cross_section_xml_path)
    else:
        print(
            "Set your $OPENMC_CROSS_SECTIONS environmental variable to "
            f"{cross_section_xml_path} to use this custom library"
        )

    return cross_section_xml_path


def download_single_file(
    url: str,
    output_filename: Union[str, Path] = None,
    destination: Union[str, Path] = None,
    overwrite: bool = True,
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

    if output_filename is None:
        local_path = Path(Path(urlparse(url).path).name)
    else:
        local_path = output_filename

    if destination is not None:
        Path(destination).mkdir(parents=True, exist_ok=True)
        local_path = destination / local_path

    if overwrite is False and local_path.is_file():
        print(f"Skipping {local_path}, already downloaded")
        return local_path

    local_path = download_url_in_chuncks(url, local_path)

    return local_path


@retry(HTTPError, tries=3)
def download_url_in_chuncks(url, local_path):
    with urlopen(url) as response:
        # Copy file to disk in chunks
        print("Downloading {}... ".format(local_path), end="")

        with open(local_path, "wb") as fh:
            while True:
                chunk = response.read(_BLOCK_SIZE)
                if not chunk:
                    break
                fh.write(chunk)
            print("")

    return local_path


def download_data_frame_of(
    dataframe: pd.DataFrame, destination: Union[str, Path], overwrite: bool = True
):
    local_files = []
    for index, row in dataframe.iterrows():
        local_file = download_single_file(
            url=row["url"],
            output_filename=row["local_file"],
            destination=destination,
            overwrite=overwrite,
        )
        local_files.append(local_file)

    return local_files


def create_cross_sections_xml(
    dataframe: pd.DataFrame, destination: Union[str, Path]
) -> str:
    library = openmc.data.DataLibrary()
    for index, row in dataframe.iterrows():
        if destination is None:
            library.register_file(Path(row["local_file"]))
        else:
            library.register_file(Path(destination) / Path(row["local_file"]))
    if destination is None:
        library.export_to_xml("cross_sections.xml")
        cross_sections_xml_path = "cross_sections.xml"
    else:
        if not isinstance(destination, Path):
            destination = Path(destination)
            destination.mkdir(parents=True, exist_ok=True)
        library.export_to_xml(destination / "cross_sections.xml")
        cross_sections_xml_path = str(destination / "cross_sections.xml")

    absolute_path = str(Path(cross_sections_xml_path).absolute())
    print(f"written cross sections xml file to {absolute_path}")

    return absolute_path


def identify_sabs_to_download(
    libraries: typing.Tuple[str],
    sabs: typing.Tuple[str],
):
    if sabs == []:
        return pd.DataFrame()
    elif sabs == "all" or sabs == ["all"]:
        sabs = SAB_OPTIONS
    elif sabs == "stable" or sabs == ["stable"]:
        sabs = SAB_OPTIONS  # todo check they are all stable, perhaps not UO2

    if len(libraries) == 0:
        raise ValueError(
            "At least one library must be selected, options are", LIB_OPTIONS
        )

    for sab in sabs:
        if sab not in SAB_OPTIONS:
            raise ValueError(
                f"Sab passing in {sab} not found in available names {SAB_OPTIONS}"
            )

    priority_dict = {}
    for counter, entry in enumerate(libraries):
        if entry not in LIB_OPTIONS:
            raise ValueError(
                f"The library must be one of the following {LIB_OPTIONS}. Not {entry}."
            )

        priority_dict[entry] = counter + 1

    print("Searching libraries with the following priority", priority_dict)

    # Tried to removed this dict to dataframe conversion out of the function
    # and into the initialization of the package but this resulted in
    # a SettingwithCopyWarning which can be fixed and understood here
    # https://www.dataquest.io/blog/settingwithcopywarning/
    xs_info_df = pd.DataFrame.from_dict(sab_xs_info)

    is_library = xs_info_df["library"].isin(libraries)
    print("Sab found matching library requirements", is_library.values.sum())

    is_particle = xs_info_df["particle"].isin(["sab"])
    print("Sab found matching particle requirements", is_particle.values.sum())

    is_sab = xs_info_df["sab"].isin(sabs)
    print("Sab found matching isotope requirements", is_sab.values.sum())

    xs_info_df = xs_info_df[(is_sab) & (is_library) & (is_particle)]

    xs_info_df["priority"] = xs_info_df["library"].map(priority_dict)

    xs_info_df = xs_info_df.sort_values(by=["priority"])

    xs_info_df = xs_info_df.drop_duplicates(subset=["sab", "particle"], keep="first")

    # end url is unique so this avoids downloading duplicates of the same file
    xs_info_df = xs_info_df.drop_duplicates(subset=["url"], keep="first")

    print("Sabs found matching all requirements", len(xs_info_df))

    return xs_info_df


def identify_isotopes_to_download(
    libraries: typing.Tuple[str],
    isotopes: typing.Tuple[str],
):
    if isotopes == []:
        return pd.DataFrame()
    elif isotopes == "all" or isotopes == ["all"]:
        isotopes = ALL_ISOTOPE_OPTIONS
    elif isotopes == "stable" or isotopes == ["stable"]:
        isotopes = STABLE_ISOTOPE_OPTIONS

    print("isotopes", isotopes)

    if len(libraries) == 0:
        raise ValueError(
            "At least one library must be selected, options are", LIB_OPTIONS
        )

    priority_dict = {}
    for counter, entry in enumerate(libraries):
        if entry not in LIB_OPTIONS:
            raise ValueError(
                f"The library must be one of the following {LIB_OPTIONS}. Not {entry}."
            )

        priority_dict[entry] = counter + 1

    print("Searching libraries with the following priority", priority_dict)

    # Tried to removed this dict to dataframe conversion out of the function
    # and into the initialization of the package but this resulted in
    # a SettingwithCopyWarning which can be fixed and understood here
    # https://www.dataquest.io/blog/settingwithcopywarning/
    xs_info_df = pd.DataFrame.from_dict(neutron_xs_info)

    is_library = xs_info_df["library"].isin(libraries)
    print("Isotopes found matching library requirements", is_library.values.sum())

    is_particle = xs_info_df["particle"].isin(["neutron"])
    print("Isotopes found matching particle requirements", is_particle.values.sum())

    is_isotope = xs_info_df["isotope"].isin(isotopes)
    print("Isotopes found matching isotope requirements", is_isotope.values.sum())

    xs_info_df = xs_info_df[(is_isotope) & (is_library) & (is_particle)]

    xs_info_df["priority"] = xs_info_df["library"].map(priority_dict)

    xs_info_df = xs_info_df.sort_values(by=["priority"])

    xs_info_df = xs_info_df.drop_duplicates(
        subset=["isotope", "particle"], keep="first"
    )

    # end url is unique so this avoids downloading duplicates of the same file
    xs_info_df = xs_info_df.drop_duplicates(subset=["url"], keep="first")

    print("Isotopes found matching all requirements", len(xs_info_df))

    return xs_info_df


def identify_elements_to_download(
    libraries: typing.Tuple[str],
    elements: typing.Tuple[str],
):
    if elements == []:
        return pd.DataFrame()
    elif elements == "all" or elements == ["all"]:
        elements = ALL_ELEMENT_OPTIONS
    elif elements == "stable" or elements == ["stable"]:
        elements = STABLE_ELEMENT_OPTIONS

    print("elements", elements)

    if len(libraries) == 0:
        raise ValueError(
            "At least one library must be selected, options are", LIB_OPTIONS
        )

    priority_dict = {}
    for counter, entry in enumerate(libraries):
        if entry not in LIB_OPTIONS:
            raise ValueError("The library must be one of the following", LIB_OPTIONS)

        priority_dict[entry] = counter + 1

    print("Searching libraries with the following priority", priority_dict)

    # Tried to removed this dict to dataframe conversion out of the function
    # and into the initialization of the package but this resulted in
    # a SettingwithCopyWarning which can be fixed and understood here
    # https://www.dataquest.io/blog/settingwithcopywarning/
    xs_info_df = pd.DataFrame.from_dict(photon_xs_info)

    is_library = xs_info_df["library"].isin(libraries)
    print("Elements found matching library requirements", is_library.values.sum())

    is_particle = xs_info_df["particle"].isin(["photon"])
    print("Elements found matching particle requirements", is_particle.values.sum())

    is_element = xs_info_df["element"].isin(elements)
    print("Elements found matching element requirements", is_element.values.sum())

    xs_info_df = xs_info_df[(is_element) & (is_library) & (is_particle)]

    xs_info_df["priority"] = xs_info_df["library"].map(priority_dict)

    xs_info_df = xs_info_df.sort_values(by=["priority"])

    xs_info_df = xs_info_df.drop_duplicates(
        subset=["element", "particle"], keep="first"
    )

    # end url is unique so this avoids downloading duplicates of the same file
    xs_info_df = xs_info_df.drop_duplicates(subset=["url"], keep="first")

    print("Elements found matching all requirements", len(xs_info_df))

    return xs_info_df


openmc.Materials.download_cross_section_data = download_cross_section_data
