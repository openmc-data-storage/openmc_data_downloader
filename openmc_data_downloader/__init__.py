try:
    # this works for python 3.7 and lower
    from importlib.metadata import version, PackageNotFoundError
except (ModuleNotFoundError, ImportError):
    # this works for python 3.8 and higher
    from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("openmc_data_downloader")
except PackageNotFoundError:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)

__all__ = ["__version__"]

from .cross_sections_directory import (
    NATURAL_ABUNDANCE,
    LIB_OPTIONS,
    PARTICLE_OPTIONS,
    SAB_OPTIONS,
    STABLE_ISOTOPE_OPTIONS,
    ALL_ISOTOPE_OPTIONS,
    xs_info,
    sab_info,
)

from .utils import (
    create_cross_sections_xml,
    just_in_time_library_generator,
    download_data_frame_of_isotopes,
    download_single_file,
    expand_elements_to_isotopes,
    expand_materials_xml_to_isotopes,
    expand_materials_xml_to_sab,
    identify_isotopes_to_download,
    expand_materials_to_isotopes,
    expand_materials_to_sabs,
    identify_sab_to_download,
)
