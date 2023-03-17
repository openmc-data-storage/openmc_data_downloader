import re
import xml.etree.ElementTree as ET
from pathlib import Path

from numpy import nested_iters

# from https://github.com/openmc-dev/openmc/blob/develop/openmc/data/data.py
# remove when pip install openmc via PyPi is available
NATURAL_ABUNDANCE = {
    "H": ["H1", "H2"],
    "He": ["He3", "He4"],
    "Li": ["Li6", "Li7"],
    "Be": ["Be9"],
    "B": ["B10", "B11"],
    "C": ["C12", "C13", "C0"],  # C0 included for ENDF/B 7.1 NNDC
    "N": ["N14", "N15"],
    "O": ["O16", "O17", "O18"],
    "F": ["F19"],
    "Ne": ["Ne20", "Ne21", "Ne22"],
    "Na": ["Na23"],
    "Mg": ["Mg24", "Mg25", "Mg26"],
    "Al": ["Al27"],
    "Si": ["Si28", "Si29", "Si30"],
    "P": ["P31"],
    "S": ["S32", "S33", "S34", "S36"],
    "Cl": ["Cl35", "Cl37"],
    "Ar": ["Ar36", "Ar38", "Ar40"],
    "K": ["K39", "K40", "K41"],
    "Ca": ["Ca40", "Ca42", "Ca43", "Ca44", "Ca46", "Ca48"],
    "Sc": ["Sc45"],
    "Ti": ["Ti46", "Ti47", "Ti48", "Ti49", "Ti50"],
    "V": ["V50", "V51"],
    "Cr": ["Cr50", "Cr52", "Cr53", "Cr54"],
    "Mn": ["Mn55"],
    "Fe": ["Fe54", "Fe56", "Fe57", "Fe58"],
    "Co": ["Co59"],
    "Ni": ["Ni58", "Ni60", "Ni61", "Ni62", "Ni64"],
    "Cu": ["Cu63", "Cu65"],
    "Zn": ["Zn64", "Zn66", "Zn67", "Zn68", "Zn70"],
    "Ga": ["Ga69", "Ga71"],
    "Ge": ["Ge70", "Ge72", "Ge73", "Ge74", "Ge76"],
    "As": ["As75"],
    "Se": ["Se74", "Se76", "Se77", "Se78", "Se80", "Se82"],
    "Br": ["Br79", "Br81"],
    "Kr": ["Kr78", "Kr80", "Kr82", "Kr83", "Kr84", "Kr86"],
    "Rb": ["Rb85", "Rb87"],
    "Sr": ["Sr84", "Sr86", "Sr87", "Sr88"],
    "Y": ["Y89"],
    "Zr": ["Zr90", "Zr91", "Zr92", "Zr94", "Zr96"],
    "Nb": ["Nb93"],
    "Mo": ["Mo92", "Mo94", "Mo95", "Mo96", "Mo97", "Mo98", "Mo100"],
    "Ru": ["Ru96", "Ru98", "Ru99", "Ru100", "Ru101", "Ru102", "Ru104"],
    "Rh": ["Rh103"],
    "Pd": ["Pd102", "Pd104", "Pd105", "Pd106", "Pd108", "Pd110"],
    "Ag": ["Ag107", "Ag109"],
    "Cd": ["Cd106", "Cd108", "Cd110", "Cd111", "Cd112", "Cd113", "Cd114", "Cd116"],
    "In": ["In113", "In115"],
    "Sn": [
        "Sn112",
        "Sn114",
        "Sn115",
        "Sn116",
        "Sn117",
        "Sn118",
        "Sn119",
        "Sn120",
        "Sn122",
        "Sn124",
    ],
    "Sb": ["Sb121", "Sb123"],
    "Te": ["Te120", "Te122", "Te123", "Te124", "Te125", "Te126", "Te128", "Te130"],
    "I": ["I127"],
    "Xe": [
        "Xe124",
        "Xe126",
        "Xe128",
        "Xe129",
        "Xe130",
        "Xe131",
        "Xe132",
        "Xe134",
        "Xe136",
    ],
    "Cs": ["Cs133"],
    "Ba": ["Ba130", "Ba132", "Ba134", "Ba135", "Ba136", "Ba137", "Ba138"],
    "La": ["La138", "La139"],
    "Ce": ["Ce136", "Ce138", "Ce140", "Ce142"],
    "Pr": ["Pr141"],
    "Nd": ["Nd142", "Nd143", "Nd144", "Nd145", "Nd146", "Nd148", "Nd150"],
    "Sm": ["Sm144", "Sm147", "Sm148", "Sm149", "Sm150", "Sm152", "Sm154"],
    "Eu": ["Eu151", "Eu153"],
    "Gd": ["Gd152", "Gd154", "Gd155", "Gd156", "Gd157", "Gd158", "Gd160"],
    "Tb": ["Tb159"],
    "Dy": ["Dy156", "Dy158", "Dy160", "Dy161", "Dy162", "Dy163", "Dy164"],
    "Ho": ["Ho165"],
    "Er": ["Er162", "Er164", "Er166", "Er167", "Er168", "Er170"],
    "Tm": ["Tm169"],
    "Yb": ["Yb168", "Yb170", "Yb171", "Yb172", "Yb173", "Yb174", "Yb176"],
    "Lu": ["Lu175", "Lu176"],
    "Hf": ["Hf174", "Hf176", "Hf177", "Hf178", "Hf179", "Hf180"],
    "Ta": ["Ta180", "Ta181"],
    "W": ["W180", "W182", "W183", "W184", "W186"],
    "Re": ["Re185", "Re187"],
    "Os": ["Os184", "Os186", "Os187", "Os188", "Os189", "Os190", "Os192"],
    "Ir": ["Ir191", "Ir193"],
    "Pt": ["Pt190", "Pt192", "Pt194", "Pt195", "Pt196", "Pt198"],
    "Au": ["Au197"],
    "Hg": ["Hg196", "Hg198", "Hg199", "Hg200", "Hg201", "Hg202", "Hg204"],
    "Tl": ["Tl203", "Tl205"],
    "Pb": ["Pb204", "Pb206", "Pb207", "Pb208"],
    "Bi": ["Bi209"],
    "Th": ["Th230", "Th232"],
    "Pa": ["Pa231"],
    "U": ["U234", "U235", "U238"],
    "Ac": [],  # no stable isotopes
    "Am": [],  # no stable isotopes
    "At": [],  # no stable isotopes
    "Bk": [],  # no stable isotopes
    "Cf": [],  # no stable isotopes
    "Cm": [],  # no stable isotopes
    "Es": [],  # no stable isotopes
    "Fm": [],  # no stable isotopes
    "Fr": [],  # no stable isotopes
    "Np": [],  # no stable isotopes
    "Pm": [],  # no stable isotopes
    "Po": [],  # no stable isotopes
    "Pu": [],  # no stable isotopes
    "Ra": [],  # no stable isotopes
    "Rn": [],  # no stable isotopes
    "Tc": [],  # no stable isotopes
}


def zaid_to_isotope(zaid: str) -> str:
    """converts an isotope into a zaid e.g. 003006 -> Li6"""
    a = str(zaid)[-3:]
    z = str(zaid)[:-3]
    symbol = ATOMIC_SYMBOL[int(z)]
    return symbol + str(int(a))


def get_isotopes_or_elements_from_xml(filename, particle_type):
    if particle_type == "sab":
        particle_type = "thermal"
    tree = ET.parse(Path(__file__).parent / filename)
    root = tree.getroot()
    neutron_isotopes = []
    for elem in root:
        if elem.attrib["type"] == particle_type:
            neutron_isotopes.append(elem.attrib["materials"])
    if len(neutron_isotopes) == 0:
        raise ValueError(f"no {particle_type} were found in {filename}")
    return neutron_isotopes


def core_dict_entry(library, name, base_url):
    entry = {}
    entry["library"] = library
    entry["remote_file"] = name + ".h5"
    entry["url"] = base_url + entry["remote_file"]
    entry["local_file"] = entry["library"] + "_" + entry["remote_file"]
    return entry


def populate_neutron_cross_section_list(isotopes, base_url, library):
    xs_info = []
    for isotope in isotopes:
        entry = core_dict_entry(library, isotope, base_url)
        entry["particle"] = "neutron"
        entry["isotope"] = isotope
        entry["element"] = re.split(r"(\d+)", entry["isotope"])[0]
        xs_info.append(entry)
    return xs_info


def populate_sab_cross_section_list(sabs, base_url, library):
    xs_info = []
    for sab in sabs:
        entry = core_dict_entry(library, sab, base_url)
        entry["particle"] = "sab"
        entry["sab"] = sab
        xs_info.append(entry)
    return xs_info


def populate_photon_cross_section_list(elements, base_url, library):
    xs_info = []
    for element in elements:
        entry = core_dict_entry(library, element, base_url)
        entry["particle"] = "photon"
        entry["element"] = element
        xs_info.append(entry)
    return xs_info


def get_isotopes_or_elements_info_from_xml(particle_type, library):
    base_url = lib_to_base_url[(library, particle_type)]
    filename = lib_to_xml[library]

    isotopes_or_elements = get_isotopes_or_elements_from_xml(filename, particle_type)

    if particle_type == "photon":
        info = populate_photon_cross_section_list(
            isotopes_or_elements, base_url, library
        )

    elif particle_type == "neutron":
        info = populate_neutron_cross_section_list(
            isotopes_or_elements, base_url, library
        )
    elif particle_type == "sab":
        info = populate_sab_cross_section_list(isotopes_or_elements, base_url, library)
    else:
        raise ValueError(
            f'particle type {particle_type} not supported, acceptable particle types are "neutron" or "photon'
        )
    return info


# {
#     'filename':
#     'particle_type':
#     'base_url':,
#     'library':
# }

lib_to_xml = {
    "FENDL-3.1d": "fendl_3.1d_cross_sections.xml",
    "ENDFB-8.0-NNDC": "nndc_8.0_cross_sections.xml",
    "ENDFB-7.1-NNDC": "nndc_7.1_cross_sections.xml",
    "TENDL-2019": "tendl_2019_cross_sections.xml",
}
lib_to_base_url = {
    (
        "FENDL-3.1d",
        "neutron",
    ): "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/neutron/",
    (
        "FENDL-3.1d",
        "photon",
    ): "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/photon/",
    (
        "ENDFB-8.0-NNDC",
        "neutron",
    ): "https://github.com/openmc-data-storage/ENDF-B-VIII.0-NNDC/raw/main/h5_files/neutron/",
    (
        "ENDFB-8.0-NNDC",
        "sab",
    ): "https://github.com/openmc-data-storage/ENDF-B-VIII.0-NNDC/raw/main/h5_files/neutron/",
    (
        "ENDFB-8.0-NNDC",
        "photon",
    ): "https://github.com/openmc-data-storage/ENDF-B-VIII.0-NNDC/raw/main/h5_files/photon/",
    (
        "ENDFB-7.1-NNDC",
        "neutron",
    ): "https://github.com/openmc-data-storage/ENDF-B-VII.1-NNDC/raw/main/h5_files/neutron/",
    (
        "ENDFB-7.1-NNDC",
        "sab",
    ): "https://github.com/openmc-data-storage/ENDF-B-VII.1-NNDC/raw/main/h5_files/neutron/",
    (
        "ENDFB-7.1-NNDC",
        "photon",
    ): "https://github.com/openmc-data-storage/ENDF-B-VII.1-NNDC/raw/main/h5_files/photon/",
    (
        "TENDL-2019",
        "neutron",
    ): "https://github.com/openmc-data-storage/TENDL-2019/raw/main/h5_files/",
}

neutron_xs_info = []
neutron_xs_info += get_isotopes_or_elements_info_from_xml("neutron", "TENDL-2019")
neutron_xs_info += get_isotopes_or_elements_info_from_xml("neutron", "ENDFB-7.1-NNDC")
neutron_xs_info += get_isotopes_or_elements_info_from_xml("neutron", "FENDL-3.1d")
neutron_xs_info += get_isotopes_or_elements_info_from_xml("neutron", "ENDFB-8.0-NNDC")

photon_xs_info = []
photon_xs_info += get_isotopes_or_elements_info_from_xml(
    "photon",
    "ENDFB-7.1-NNDC",
)
photon_xs_info += get_isotopes_or_elements_info_from_xml("photon", "FENDL-3.1d")
photon_xs_info += get_isotopes_or_elements_info_from_xml("photon", "ENDFB-8.0-NNDC")

sab_xs_info = []
sab_xs_info += get_isotopes_or_elements_info_from_xml(
    "sab",
    "ENDFB-7.1-NNDC",
)
sab_xs_info += get_isotopes_or_elements_info_from_xml("sab", "ENDFB-8.0-NNDC")

ATOMIC_SYMBOL = {
    0: "n",
    1: "H",
    2: "He",
    3: "Li",
    4: "Be",
    5: "B",
    6: "C",
    7: "N",
    8: "O",
    9: "F",
    10: "Ne",
    11: "Na",
    12: "Mg",
    13: "Al",
    14: "Si",
    15: "P",
    16: "S",
    17: "Cl",
    18: "Ar",
    19: "K",
    20: "Ca",
    21: "Sc",
    22: "Ti",
    23: "V",
    24: "Cr",
    25: "Mn",
    26: "Fe",
    27: "Co",
    28: "Ni",
    29: "Cu",
    30: "Zn",
    31: "Ga",
    32: "Ge",
    33: "As",
    34: "Se",
    35: "Br",
    36: "Kr",
    37: "Rb",
    38: "Sr",
    39: "Y",
    40: "Zr",
    41: "Nb",
    42: "Mo",
    43: "Tc",
    44: "Ru",
    45: "Rh",
    46: "Pd",
    47: "Ag",
    48: "Cd",
    49: "In",
    50: "Sn",
    51: "Sb",
    52: "Te",
    53: "I",
    54: "Xe",
    55: "Cs",
    56: "Ba",
    57: "La",
    58: "Ce",
    59: "Pr",
    60: "Nd",
    61: "Pm",
    62: "Sm",
    63: "Eu",
    64: "Gd",
    65: "Tb",
    66: "Dy",
    67: "Ho",
    68: "Er",
    69: "Tm",
    70: "Yb",
    71: "Lu",
    72: "Hf",
    73: "Ta",
    74: "W",
    75: "Re",
    76: "Os",
    77: "Ir",
    78: "Pt",
    79: "Au",
    80: "Hg",
    81: "Tl",
    82: "Pb",
    83: "Bi",
    84: "Po",
    85: "At",
    86: "Rn",
    87: "Fr",
    88: "Ra",
    89: "Ac",
    90: "Th",
    91: "Pa",
    92: "U",
    93: "Np",
    94: "Pu",
    95: "Am",
    96: "Cm",
    97: "Bk",
    98: "Cf",
    99: "Es",
    100: "Fm",
    101: "Md",
    102: "No",
    103: "Lr",
    104: "Rf",
    105: "Db",
    106: "Sg",
    107: "Bh",
    108: "Hs",
    109: "Mt",
    110: "Ds",
    111: "Rg",
    112: "Cn",
    113: "Nh",
    114: "Fl",
    115: "Mc",
    116: "Lv",
    117: "Ts",
    118: "Og",
}


all_libs = []
for entry in neutron_xs_info:
    all_libs.append(entry["library"])

LIB_OPTIONS = list(set(all_libs))
PARTICLE_OPTIONS = ["neutron", "photon", "sab"]

nested_list = list(NATURAL_ABUNDANCE.values())

# should this come from the isotopes available in the xml files
STABLE_ISOTOPE_OPTIONS = [item for sublist in nested_list for item in sublist]

ALL_ISOTOPE_OPTIONS = []
for xml in [
    "tendl_2019_cross_sections.xml",
    "nndc_7.1_cross_sections.xml",
    "nndc_8.0_cross_sections.xml",
    "fendl_3.1d_cross_sections.xml",
]:
    isotopes = get_isotopes_or_elements_from_xml(xml, "neutron")
    ALL_ISOTOPE_OPTIONS = ALL_ISOTOPE_OPTIONS + isotopes

SAB_OPTIONS = []
for xml in [
    "nndc_7.1_cross_sections.xml",
    "nndc_8.0_cross_sections.xml",
]:
    sabs = get_isotopes_or_elements_from_xml(xml, "sab")
    SAB_OPTIONS = SAB_OPTIONS + sabs

ALL_ISOTOPE_OPTIONS = sorted(list(set(ALL_ISOTOPE_OPTIONS)))

ALL_ELEMENT_OPTIONS = sorted(
    list(set([re.split(r"(\d+)", i)[0] for i in ALL_ISOTOPE_OPTIONS]))
)
STABLE_ELEMENT_OPTIONS = sorted(
    list(set([re.split(r"(\d+)", i)[0] for i in STABLE_ISOTOPE_OPTIONS]))
)
