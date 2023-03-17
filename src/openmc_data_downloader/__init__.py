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
    STABLE_ISOTOPE_OPTIONS,
    ALL_ISOTOPE_OPTIONS,
    ALL_ELEMENT_OPTIONS,
    STABLE_ELEMENT_OPTIONS,
    SAB_OPTIONS,
    neutron_xs_info,
    photon_xs_info,
    sab_xs_info,
)

from .utils import (
    create_cross_sections_xml,
    download_single_file,
    identify_isotopes_to_download,
    identify_sabs_to_download,
    expand_materials_to_isotopes,
    expand_materials_to_sabs,
)
