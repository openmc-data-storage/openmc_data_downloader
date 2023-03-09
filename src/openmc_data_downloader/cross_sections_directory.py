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

    tree = ET.parse(Path(__file__).parent/filename)
    root = tree.getroot()
    neutron_isotopes = []
    for elem in root:
        if elem.attrib['type'] == particle_type:
            neutron_isotopes.append(elem.attrib['materials'])
    if len(neutron_isotopes) == 0:
        raise ValueError(f'no {particle_type} were found in {filename}')
    return neutron_isotopes


tendl_2019_neutron_isotopes = get_isotopes_or_elements_from_xml('tendl_2019_cross_sections.xml', 'neutron')

endfb_71_nndc_photon_elements = get_isotopes_or_elements_from_xml('nndc_7.1_cross_sections.xml', 'photon')
endfb_71_nndc_neutron_isotopes = get_isotopes_or_elements_from_xml('nndc_7.1_cross_sections.xml', 'neutron')

fendl_31d_neutron_isotopes = get_isotopes_or_elements_from_xml('fendl_3.1d_cross_sections.xml', "neutron")
fendl_31d_photon_elements = get_isotopes_or_elements_from_xml('fendl_3.1d_cross_sections.xml', "photon")


tendl_2019_base_url = (
    "https://github.com/openmc-data-storage/TENDL-2019/raw/main/h5_files/"
)

tendl_2019_xs_info = []
for isotope in tendl_2019_neutron_isotopes:
    entry = {}
    entry["isotope"] = isotope
    entry["particle"] = "neutron"
    entry["library"] = "TENDL-2019"
    entry["remote_file"] = entry["isotope"] + ".h5"
    entry["url"] = tendl_2019_base_url + entry["remote_file"]
    entry["element"] = re.split(r"(\d+)", entry["isotope"])[0]
    entry["local_file"] = entry["library"] + "_" + entry["remote_file"]
    tendl_2019_xs_info.append(entry)
    # could add size of file in mb as well



endfb_71_nndc_base_url = (
    "https://github.com/openmc-data-storage/ENDF-B-VII.1-NNDC/raw/main/h5_files/"
)

endfb_71_nndc_xs_info = []
for isotope in endfb_71_nndc_neutron_isotopes:
    entry = {}
    entry["isotope"] = isotope
    entry["particle"] = "neutron"
    entry["library"] = "ENDFB-7.1-NNDC"
    entry["remote_file"] = entry["isotope"] + ".h5"
    entry["url"] = endfb_71_nndc_base_url + "neutron/" + entry["remote_file"]
    entry["element"] = re.split(r"(\d+)", entry["isotope"])[0]
    entry["local_file"] = entry["library"] + "_" + entry["remote_file"]
    endfb_71_nndc_xs_info.append(entry)
    # could add size of file in mb as well


for element in endfb_71_nndc_photon_elements:
    for isotope in NATURAL_ABUNDANCE[element]:
        entry = {}
        # perhaps there is a better way of doing this
        entry["isotope"] = isotope
        entry["particle"] = "photon"
        entry["library"] = "ENDFB-7.1-NNDC"
        entry["remote_file"] = element + ".h5"
        entry["url"] = endfb_71_nndc_base_url + "photon/" + entry["remote_file"]
        entry["element"] = element
        entry["local_file"] = entry["library"] + "_" + entry["remote_file"]
        endfb_71_nndc_xs_info.append(entry)

# TODO see if we can use this approach for thermal list
# tree = ET.parse(Path(__file__).parent/'nndc_7.1_cross_sections.xml')
# root = tree.getroot()
# endfb_71_nndc_thermal = []
# for elem in root:
#     if elem.attrib['type'] == 'thermal':
#         endfb_71_nndc_thermal.append(elem.attrib['materials'])

endfb_71_nndc_thermal = [
    "c_Al27",
    "c_Be",
    "c_Be_in_BeO",
    "c_C6H6",
    "c_D_in_D2O",
    "c_Fe56",
    "c_Graphite",
    "c_H_in_CH2",
    "c_H_in_CH4_liquid",
    "c_H_in_CH4_solid",
    "c_H_in_H2O",
    "c_H_in_ZrH",
    "c_O_in_BeO",
    "c_O_in_UO2",
    "c_U_in_UO2",
    "c_Zr_in_ZrH",
    "c_ortho_D",
    "c_ortho_H",
    "c_para_D",
    "c_para_H",
]


endfb_71_nndc_sab_info = []
for name in endfb_71_nndc_thermal:
    entry = {}
    # perhaps there is a better way of doing this
    entry["name"] = name
    entry["particle"] = "thermal"
    entry["library"] = "ENDFB-7.1-NNDC"
    entry["remote_file"] = name + ".h5"
    entry["url"] = endfb_71_nndc_base_url + "neutron/" + entry["remote_file"]
    entry["local_file"] = entry["library"] + "_" + entry["remote_file"]
    endfb_71_nndc_sab_info.append(entry)

fendl_31d_base_url = (
    "https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/"
)

fendl_31d_xs_info = []
for isotope in fendl_31d_neutron_isotopes:
    entry = {}
    entry["isotope"] = isotope
    entry["particle"] = "neutron"
    entry["library"] = "FENDL-3.1d"
    entry["remote_file"] = entry["isotope"] + ".h5"
    entry["url"] = fendl_31d_base_url + "neutron/" + entry["remote_file"]
    entry["element"] = re.split(r"(\d+)", entry["isotope"])[0]
    entry["local_file"] = entry["library"] + "_" + entry["remote_file"]
    fendl_31d_xs_info.append(entry)
    # could add size of file in mb as well


for element in fendl_31d_photon_elements:
    for isotope in NATURAL_ABUNDANCE[element]:
        entry = {}
        # perhaps there is a better way of doing this
        entry["isotope"] = isotope
        entry["particle"] = "photon"
        entry["library"] = "FENDL-3.1d"
        entry["remote_file"] = element + ".h5"
        entry["url"] = fendl_31d_base_url + "photon/" + entry["remote_file"]
        entry["element"] = element
        entry["local_file"] = entry["library"] + "_" + entry["remote_file"]
        fendl_31d_xs_info.append(entry)


endfb_71_wmp_neutron_isotopes = [
    "001001",
    "001002",
    "001003",
    "002003",
    "002004",
    "003006",
    "003007",
    "004007",
    "004009",
    "005010",
    "005011",
    "006000",
    "007014",
    "007015",
    "008016",
    "008017",
    "009019",
    "011022",
    "011023",
    "012024",
    "012025",
    "012026",
    "013027",
    "014028",
    "014029",
    "014030",
    "015031",
    "016032",
    "016033",
    "016034",
    "016036",
    "017035",
    "017037",
    "018036",
    "018038",
    "018040",
    "019039",
    "019040",
    "019041",
    "020040",
    "020042",
    "020043",
    "020044",
    "020046",
    "020048",
    "021045",
    "022046",
    "022047",
    "022048",
    "022049",
    "022050",
    "023050",
    "023051",
    "024050",
    "024052",
    "024053",
    "024054",
    "025055",
    "026054",
    "026056",
    "026057",
    "026058",
    "027058",
    "027058m1",
    "027059",
    "028058",
    "028059",
    "028060",
    "028061",
    "028062",
    "028064",
    "029063",
    "029065",
    "030064",
    "030065",
    "030066",
    "030067",
    "030068",
    "030070",
    "031069",
    "031071",
    "032070",
    "032072",
    "032073",
    "032074",
    "032076",
    "033074",
    "033075",
    "034074",
    "034076",
    "034077",
    "034078",
    "034079",
    "034080",
    "034082",
    "035079",
    "035081",
    "036078",
    "036080",
    "036082",
    "036083",
    "036084",
    "036085",
    "036086",
    "037085",
    "037086",
    "037087",
    "038084",
    "038086",
    "038087",
    "038088",
    "038089",
    "038090",
    "039089",
    "039090",
    "039091",
    "040090",
    "040091",
    "040092",
    "040093",
    "040094",
    "040095",
    "040096",
    "041093",
    "041094",
    "041095",
    "042092",
    "042094",
    "042095",
    "042096",
    "042097",
    "042098",
    "042099",
    "042100",
    "043099",
    "044096",
    "044098",
    "044099",
    "044100",
    "044101",
    "044102",
    "044103",
    "044104",
    "044105",
    "044106",
    "045103",
    "045105",
    "046102",
    "046104",
    "046105",
    "046106",
    "046107",
    "046108",
    "046110",
    "047107",
    "047109",
    "047110m1",
    "047111",
    "048106",
    "048108",
    "048110",
    "048111",
    "048112",
    "048113",
    "048114",
    "048115m1",
    "048116",
    "049113",
    "049115",
    "050112",
    "050113",
    "050114",
    "050115",
    "050116",
    "050117",
    "050118",
    "050119",
    "050120",
    "050122",
    "050123",
    "050124",
    "050125",
    "050126",
    "051121",
    "051123",
    "051124",
    "051125",
    "051126",
    "052120",
    "052122",
    "052123",
    "052124",
    "052125",
    "052126",
    "052127m1",
    "052128",
    "052129m1",
    "052130",
    "052132",
    "053127",
    "053129",
    "053130",
    "053131",
    "053135",
    "054123",
    "054124",
    "054126",
    "054128",
    "054129",
    "054130",
    "054131",
    "054132",
    "054133",
    "054134",
    "054135",
    "054136",
    "055133",
    "055134",
    "055135",
    "055136",
    "055137",
    "056130",
    "056132",
    "056133",
    "056134",
    "056135",
    "056136",
    "056137",
    "056138",
    "056140",
    "057138",
    "057139",
    "057140",
    "058136",
    "058138",
    "058139",
    "058140",
    "058141",
    "058142",
    "058143",
    "058144",
    "059141",
    "059142",
    "059143",
    "060142",
    "060143",
    "060144",
    "060145",
    "060146",
    "060147",
    "060148",
    "060150",
    "061147",
    "061148",
    "061148m1",
    "061149",
    "061151",
    "062144",
    "062147",
    "062148",
    "062149",
    "062150",
    "062151",
    "062152",
    "062153",
    "062154",
    "063151",
    "063152",
    "063153",
    "063154",
    "063155",
    "063156",
    "063157",
    "064152",
    "064153",
    "064154",
    "064155",
    "064156",
    "064157",
    "064158",
    "064160",
    "065159",
    "065160",
    "066156",
    "066158",
    "066160",
    "066161",
    "066162",
    "066163",
    "066164",
    "067165",
    "067166m1",
    "068162",
    "068164",
    "068166",
    "068167",
    "068168",
    "068170",
    "069168",
    "069169",
    "069170",
    "071175",
    "071176",
    "072174",
    "072176",
    "072177",
    "072178",
    "072179",
    "072180",
    "073180",
    "073181",
    "073182",
    "074180",
    "074182",
    "074183",
    "074184",
    "074186",
    "075185",
    "075187",
    "077191",
    "077193",
    "079197",
    "080196",
    "080198",
    "080199",
    "080200",
    "080201",
    "080202",
    "080204",
    "081203",
    "081205",
    "082204",
    "082206",
    "082207",
    "082208",
    "083209",
    "088223",
    "088224",
    "088225",
    "088226",
    "089225",
    "089226",
    "089227",
    "090227",
    "090228",
    "090229",
    "090230",
    "090231",
    "090232",
    "090233",
    "090234",
    "091229",
    "091230",
    "091231",
    "091232",
    "091233",
    "092230",
    "092231",
    "092232",
    "092233",
    "092234",
    "092235",
    "092236",
    "092237",
    "092238",
    "092239",
    "092240",
    "092241",
    "093234",
    "093235",
    "093236",
    "093237",
    "093238",
    "093239",
    "094236",
    "094237",
    "094238",
    "094239",
    "094240",
    "094241",
    "094242",
    "094243",
    "094244",
    "094246",
    "095240",
    "095241",
    "095242",
    "095242m1",
    "095243",
    "095244",
    "095244m1",
    "096240",
    "096241",
    "096242",
    "096243",
    "096244",
    "096245",
    "096246",
    "096247",
    "096248",
    "096249",
    "096250",
    "097245",
    "097246",
    "097247",
    "097248",
    "097249",
    "097250",
    "098246",
    "098248",
    "098249",
    "098250",
    "098251",
    "098252",
    "098253",
    "098254",
    "099251",
    "099252",
    "099253",
    "099254",
    "099254m1",
    "099255",
    "100255",
]

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


endf_71_wmp_base_url = (
    "https://github.com/openmc-data-storage/ENDF-B-VII.1-WMP/raw/master/WMP_Library/"
)

endfb_71_wmp_xs_info = []
for zaid in endfb_71_wmp_neutron_isotopes:
    if not zaid.endswith("m1"):  # avoids meta stable files
        entry = {}
        entry["isotope"] = zaid_to_isotope(zaid)
        entry["particle"] = "neutron"
        entry["library"] = "ENDFB-7.1-WMP"
        entry["remote_file"] = zaid + ".h5"
        entry["url"] = endf_71_wmp_base_url + entry["remote_file"]
        entry["element"] = re.split(r"(\d+)", entry["isotope"])[0]
        entry["local_file"] = entry["library"] + "_" + zaid_to_isotope(zaid) + ".h5"
        endfb_71_wmp_xs_info.append(entry)
        # could add size of file in mb as well

xs_info = (
    endfb_71_nndc_xs_info
    + tendl_2019_xs_info
    + fendl_31d_xs_info
    + endfb_71_wmp_xs_info
)

sab_info = endfb_71_nndc_sab_info  # + JEFF 3.2 also contains sab

all_libs = []
for entry in xs_info:
    all_libs.append(entry["library"])

LIB_OPTIONS = list(set(all_libs))
PARTICLE_OPTIONS = ["neutron", "photon"]
SAB_OPTIONS = [
    "c_Al27",
    "c_Al_in_Sapphire",
    "c_Be",
    "c_BeO",
    "c_Be_in_BeO",
    "c_Be_in_Be2C",
    "c_C6H6",
    "c_C_in_SiC",
    "c_Ca_in_CaH2",
    "c_D_in_D2O",
    "c_D_in_D2O_ice",
    "c_Fe56",
    "c_Graphite",
    "c_Graphite_10p",
    "c_Graphite_30p",
    "c_H_in_CaH2",
    "c_H_in_CH2",
    "c_H_in_CH4_liquid",
    "c_H_in_CH4_solid",
    "c_H_in_CH4_solid_phase_II",
    "c_H_in_H2O",
    "c_H_in_H2O_solid",
    "c_H_in_C5O2H8",
    "c_H_in_Mesitylene",
    "c_H_in_Toluene",
    "c_H_in_YH2",
    "c_H_in_ZrH",
    "c_Mg24",
    "c_O_in_Sapphire",
    "c_O_in_BeO",
    "c_O_in_D2O",
    "c_O_in_H2O_ice",
    "c_O_in_UO2",
    "c_N_in_UN",
    "c_ortho_D",
    "c_ortho_H",
    "c_Si28",
    "c_Si_in_SiC",
    "c_SiO2_alpha",
    "c_SiO2_beta",
    "c_para_D",
    "c_para_H",
    "c_U_in_UN",
    "c_U_in_UO2",
    "c_Y_in_YH2",
    "c_Zr_in_ZrH",
]
nested_list = list(NATURAL_ABUNDANCE.values())
STABLE_ISOTOPE_OPTIONS = [item for sublist in nested_list for item in sublist]
ALL_ISOTOPE_OPTIONS = (
    tendl_2019_neutron_isotopes
    + fendl_31d_neutron_isotopes
    + endfb_71_nndc_neutron_isotopes
)
