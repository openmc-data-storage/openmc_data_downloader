
import re


NATURAL_ABUNDANCE = {
    'H': ['H1', 'H2'],
    'He': ['He3', 'He4', 'Li6', 'Li7'],
    'Be': ['Be9'],
    'B': ['B10', 'B11'],
    'C': ['C12', 'C13', 'C0'],  # C0 included for ENDF/B 7.1 NNDC
    'N': ['N14', 'N15'],
    'O': ['O16', 'O17', 'O18'],
    'F': ['F19'],
    'Ne': ['Ne20', 'Ne21', 'Ne22'],
    'Na': ['Na23'],
    'Mg': ['Mg24', 'Mg25', 'Mg26'],
    'Al': ['Al27'],
    'Si': ['Si28', 'Si29', 'Si30'],
    'P': ['P31'],
    'S': ['S32', 'S33', 'S34', 'S36'],
    'Cl': ['Cl35', 'Cl37'],
    'Ar': ['Ar36', 'Ar38', 'Ar40'],
    'K': ['K39', 'K40', 'K41'],
    'Ca': ['Ca40', 'Ca42', 'Ca43', 'Ca44', 'Ca46', 'Ca48'],
    'Sc': ['Sc45'],
    'Ti': ['Ti46', 'Ti47', 'Ti48', 'Ti49', 'Ti50'],
    'V': ['V50', 'V51'],
    'Cr': ['Cr50', 'Cr52', 'Cr53', 'Cr54'],
    'Mn': ['Mn55'],
    'Fe': ['Fe54', 'Fe56', 'Fe57', 'Fe58'],
    'Co': ['Co59'],
    'Ni': ['Ni58', 'Ni60', 'Ni61', 'Ni62', 'Ni64'],
    'Cu': ['Cu63', 'Cu65'],
    'Zn': ['Zn64', 'Zn66', 'Zn67', 'Zn68', 'Zn70'],
    'Ga': ['Ga69', 'Ga71', 'Ge70', 'Ge72', 'Ge73', 'Ge74', 'Ge76'],
    'As': ['As75'],
    'Se': ['Se74', 'Se76', 'Se77', 'Se78', 'Se80', 'Se82'],
    'Br': ['Br79', 'Br81'],
    'Kr': ['Kr78', 'Kr80', 'Kr82', 'Kr83', 'Kr84', 'Kr86'],
    'Rb': ['Rb85', 'Rb87'],
    'Sr': ['Sr84', 'Sr86', 'Sr87', 'Sr88'],
    'Y': ['Y89'],
    'Zr': ['Zr90', 'Zr91', 'Zr92', 'Zr94', 'Zr96'],
    'Nb': ['Nb93'],
    'Mo': ['Mo92', 'Mo94', 'Mo95', 'Mo96', 'Mo97', 'Mo98', 'Mo100', 'Ru96'],
    'Ru': ['Ru98', 'Ru99', 'Ru100', 'Ru101', 'Ru102', 'Ru104', 'Rh103'],
    'Pd': ['Pd102', 'Pd104', 'Pd105', 'Pd106', 'Pd108', 'Pd110'],
    'Ag': ['Ag107', 'Ag109'],
    'Cd': ['Cd106', 'Cd108', 'Cd110', 'Cd111', 'Cd112', 'Cd113', 'Cd114', 'Cd116'],
    'In': ['In113', 'In115'],
    'Sn': ['Sn112', 'Sn114', 'Sn115', 'Sn116', 'Sn117', 'Sn118', 'Sn119', 'Sn120', 'Sn122', 'Sn124', 'Sb121', 'Sb123'],
    'Te': ['Te120', 'Te122', 'Te123', 'Te124', 'Te125', 'Te126', 'Te128', 'Te130', 'I127'],
    'Xe': ['Xe124', 'Xe126', 'Xe128', 'Xe129', 'Xe130', 'Xe131', 'Xe132', 'Xe134', 'Xe136'],
    'Cs': ['Cs133'],
    'Ba': ['Ba130', 'Ba132', 'Ba134', 'Ba135', 'Ba136', 'Ba137', 'Ba138'],
    'La': ['La138', 'La139'],
    'Ce': ['Ce136', 'Ce138', 'Ce140', 'Ce142'],
    'Pr': ['Pr141'],
    'Nd': ['Nd142', 'Nd143', 'Nd144', 'Nd145', 'Nd146', 'Nd148', 'Nd150'],
    'Sm': ['Sm144', 'Sm147', 'Sm148', 'Sm149', 'Sm150', 'Sm152', 'Sm154'],
    'Eu': ['Eu151', 'Eu153'],
    'Gd': ['Gd152', 'Gd154', 'Gd155', 'Gd156', 'Gd157', 'Gd158', 'Gd160'],
    'Tb': ['Tb159'],
    'Dy': ['Dy156', 'Dy158', 'Dy160', 'Dy161', 'Dy162', 'Dy163', 'Dy164'],
    'Ho': ['Ho165'],
    'Er': ['Er162', 'Er164', 'Er166', 'Er167', 'Er168', 'Er170'],
    'Tm': ['Tm169'],
    'Yb': ['Yb168', 'Yb170', 'Yb171', 'Yb172', 'Yb173', 'Yb174', 'Yb176', 'Lu175', 'Lu176'],
    'Hf': ['Hf174', 'Hf176', 'Hf177', 'Hf178', 'Hf179', 'Hf180'],
    'Ta': ['Ta180', 'Ta181'],
    'W': ['W180', 'W182', 'W183', 'W184', 'W186'],
    'Re': ['Re185', 'Re187'],
    'Os': ['Os184', 'Os186', 'Os187', 'Os188', 'Os189', 'Os190', 'Os192'],
    'Ir': ['Ir191', 'Ir193'],
    'Pt': ['Pt190', 'Pt192', 'Pt194', 'Pt195', 'Pt196', 'Pt198'],
    'Au': ['Au197'],
    'Hg': ['Hg196', 'Hg198', 'Hg199', 'Hg200', 'Hg201', 'Hg202', 'Hg204'],
    'Tl': ['Tl203', 'Tl205'],
    'Pb': ['Pb204', 'Pb206', 'Pb207', 'Pb208'],
    'Bi': ['Bi209'],
    'Th': ['Th230', 'Th232'],
    'Pa': ['Pa231'],
    'U': ['U234', 'U235', 'U238'],
}


tendl_2019_isotopes = [
    'Ac225', 'Ac226', 'Ac227', 'Ag106_m1', 'Ag107', 'Ag108', 'Ag109', 'Ag110',
    'Ag110_m1', 'Ag111', 'Ag112', 'Ag113', 'Ag114', 'Ag115', 'Ag116', 'Ag117',
    'Ag118_m1', 'Al26', 'Al26_m1', 'Al27', 'Am240', 'Am241', 'Am242',
    'Am242_m1', 'Am243', 'Am244', 'Am244_m1', 'Ar36', 'Ar37', 'Ar38', 'Ar39',
    'Ar40', 'Ar41', 'As71', 'As72', 'As73', 'As74', 'As75', 'As76', 'As77',
    'Au197', 'B10', 'B11', 'Ba130', 'Ba131', 'Ba132', 'Ba133', 'Ba134',
    'Ba135', 'Ba136', 'Ba137', 'Ba138', 'Ba139', 'Ba140', 'Be7', 'Be9',
    'Bi208', 'Bi209', 'Bi210', 'Bi210_m1', 'Bk245', 'Bk246', 'Bk247', 'Bk248',
    'Bk249', 'Bk250', 'Br77', 'Br79', 'Br80', 'Br81', 'Br82', 'C12', 'C13',
    'Ca40', 'Ca41', 'Ca42', 'Ca43', 'Ca44', 'Ca45', 'Ca46', 'Ca47', 'Ca48',
    'Cd106', 'Cd107', 'Cd108', 'Cd109', 'Cd110', 'Cd111', 'Cd112', 'Cd113',
    'Cd114', 'Cd115_m1', 'Cd116', 'Ce136', 'Ce137', 'Ce137_m1', 'Ce138',
    'Ce139', 'Ce140', 'Ce141', 'Ce142', 'Ce143', 'Ce144', 'Cf246', 'Cf247',
    'Cf248', 'Cf249', 'Cf250', 'Cf251', 'Cf252', 'Cf253', 'Cf254', 'Cl35',
    'Cl36', 'Cl37', 'Cm240', 'Cm241', 'Cm242', 'Cm243', 'Cm244', 'Cm245',
    'Cm246', 'Cm247', 'Cm248', 'Cm249', 'Cm250', 'Co56', 'Co57', 'Co58',
    'Co58_m1', 'Co59', 'Co60', 'Co62_m1', 'Cr50', 'Cr51', 'Cr52', 'Cr53',
    'Cr54', 'Cs133', 'Cs134', 'Cs135', 'Cs136', 'Cs137', 'Cu63', 'Cu64',
    'Cu65', 'Cu66', 'Cu67', 'Dy154', 'Dy155', 'Dy156', 'Dy157', 'Dy158',
    'Dy159', 'Dy160', 'Dy161', 'Dy162', 'Dy163', 'Dy164', 'Dy165', 'Er162',
    'Er163', 'Er164', 'Er165', 'Er166', 'Er167', 'Er168', 'Er169', 'Er170',
    'Er171', 'Er172', 'Es251', 'Es252', 'Es253',
    'Es254', 'Es254_m1', 'Es255', 'Eu151', 'Eu152',
    'Eu152_m1', 'Eu153', 'Eu154', 'Eu155', 'Eu156', 'Eu157',
    'F19', 'Fe54', 'Fe55', 'Fe56', 'Fe57', 'Fe58', 'Fe59',
    'Fe60', 'Fm255', 'Ga67', 'Ga69', 'Ga70', 'Ga71',
    'Gd148', 'Gd149', 'Gd150', 'Gd151', 'Gd152', 'Gd153',
    'Gd154', 'Gd155', 'Gd156', 'Gd157', 'Gd158', 'Gd159',
    'Gd160', 'Gd161', 'Ge70', 'Ge71', 'Ge72', 'Ge73',
    'Ge74', 'Ge75', 'Ge76', 'H1', 'H2', 'H3', 'He3',
    'He4', 'Hf174', 'Hf175', 'Hf176', 'Hf177', 'Hf178',
    'Hf179', 'Hf180', 'Hf181', 'Hf182', 'Hg196', 'Hg197',
    'Hg197_m1', 'Hg198', 'Hg199', 'Hg200', 'Hg201', 'Hg202',
    'Hg203', 'Hg204', 'Ho163', 'Ho165', 'Ho166_m1', 'I126',
    'I127', 'I128', 'I129', 'I130', 'I131', 'I132',
    'I132_m1', 'I133', 'I134', 'I135', 'In113', 'In114',
    'In115', 'Ir190', 'Ir191', 'Ir192', 'Ir193', 'Ir194_m1',
    'K39', 'K40', 'K41', 'Kr78', 'Kr79', 'Kr80', 'Kr81',
    'Kr82', 'Kr83', 'Kr84', 'Kr85', 'Kr86', 'La137',
    'La138', 'La139', 'La140', 'Li6', 'Li7', 'Lu173',
    'Lu174', 'Lu175', 'Lu176', 'Lu177', 'Mg24', 'Mg25',
    'Mg26', 'Mg27', 'Mn52', 'Mn53', 'Mn54', 'Mn55',
    'Mo100', 'Mo92', 'Mo93', 'Mo94', 'Mo95', 'Mo96',
    'Mo97', 'Mo98', 'Mo99', 'N14', 'N15', 'Na22', 'Na23',
    'Nb91', 'Nb92', 'Nb93', 'Nb94', 'Nb94_m1', 'Nb95',
    'Nd142', 'Nd143', 'Nd144', 'Nd145', 'Nd146', 'Nd147',
    'Nd148', 'Nd149', 'Nd150', 'Ne20', 'Ne21', 'Ne22',
    'Ni56', 'Ni57', 'Ni58', 'Ni59', 'Ni60', 'Ni61',
    'Ni62', 'Ni63', 'Ni64', 'Ni66', 'Np234', 'Np235',
    'Np236', 'Np236_m1', 'Np237', 'Np238', 'Np239', 'O16',
    'O17', 'O18', 'Os184', 'Os185', 'Os186', 'Os187',
    'Os188', 'Os189', 'Os190', 'Os191', 'Os192', 'Os193',
    'P31', 'P32', 'P33', 'Pa229', 'Pa230', 'Pa231',
    'Pa232', 'Pa233', 'Pb204', 'Pb205', 'Pb206', 'Pb207',
    'Pb208', 'Pd102', 'Pd103', 'Pd104', 'Pd105', 'Pd106',
    'Pd107', 'Pd108', 'Pd109', 'Pd110', 'Pm143', 'Pm144',
    'Pm145', 'Pm146', 'Pm147', 'Pm148', 'Pm148_m1', 'Pm149',
    'Pm150', 'Pm151', 'Po208', 'Po209', 'Po210', 'Pr141',
    'Pr142', 'Pr143', 'Pt190', 'Pt191', 'Pt192', 'Pt193',
    'Pt194', 'Pt195', 'Pt196', 'Pt197', 'Pt198', 'Pu236',
    'Pu237', 'Pu238', 'Pu239', 'Pu240', 'Pu241', 'Pu242',
    'Pu243', 'Pu244', 'Pu245', 'Pu246', 'Ra223', 'Ra224',
    'Ra225', 'Ra226', 'Rb85', 'Rb86', 'Rb87', 'Rb88',
    'Re185', 'Re186', 'Re186_m1', 'Re187', 'Re188', 'Rh101',
    'Rh102', 'Rh103', 'Rh104', 'Rh105', 'Rh99', 'Ru100',
    'Ru101', 'Ru102', 'Ru103', 'Ru104', 'Ru105', 'Ru106',
    'Ru96', 'Ru97', 'Ru98', 'Ru99', 'S32', 'S33', 'S34',
    'S35', 'S36', 'Sb121', 'Sb122', 'Sb123', 'Sb124',
    'Sb125', 'Sb126', 'Sb127', 'Sc44', 'Sc45', 'Sc46',
    'Sc47', 'Sc48', 'Se74', 'Se75', 'Se76', 'Se77',
    'Se78', 'Se79', 'Se80', 'Se81', 'Se82', 'Si28',
    'Si29', 'Si30', 'Si31', 'Si32', 'Sm144', 'Sm145',
    'Sm146', 'Sm147', 'Sm148', 'Sm149', 'Sm150', 'Sm151',
    'Sm152', 'Sm153', 'Sm154', 'Sn112', 'Sn113', 'Sn114',
    'Sn115', 'Sn116', 'Sn117', 'Sn118', 'Sn119', 'Sn120',
    'Sn121', 'Sn121_m1', 'Sn122', 'Sn123', 'Sn124', 'Sn125',
    'Sn126', 'Sr83', 'Sr84', 'Sr85', 'Sr86', 'Sr87',
    'Sr88', 'Sr89', 'Sr90', 'Ta179', 'Ta180', 'Ta180_m1',
    'Ta181', 'Ta182', 'Tb158', 'Tb159', 'Tb160', 'Tb161',
    'Tc96', 'Tc97', 'Tc98', 'Tc99', 'Te120', 'Te121',
    'Te121_m1', 'Te122', 'Te123', 'Te124', 'Te125', 'Te126',
    'Te127_m1', 'Te128', 'Te129_m1', 'Te130', 'Te131',
    'Te131_m1', 'Te132', 'Th227', 'Th228', 'Th229', 'Th230',
    'Th231', 'Th232', 'Th233', 'Th234', 'Ti44', 'Ti46',
    'Ti47', 'Ti48', 'Ti49', 'Ti50', 'Tl202', 'Tl203',
    'Tl204', 'Tl205', 'Tm168', 'Tm169', 'Tm170', 'Tm171',
    'U230', 'U231', 'U232', 'U233', 'U234', 'U235',
    'U236', 'U237', 'U238', 'U239', 'U240', 'U241',
    'V48', 'V49', 'V50', 'V51', 'W180', 'W181', 'W182',
    'W183', 'W184', 'W185', 'W186', 'W188', 'Xe123',
    'Xe124', 'Xe125', 'Xe126', 'Xe127', 'Xe128', 'Xe129',
    'Xe130', 'Xe131', 'Xe132', 'Xe133', 'Xe134', 'Xe135',
    'Xe135_m1', 'Xe136', 'Y87', 'Y88', 'Y89', 'Y90',
    'Y91', 'Yb168', 'Yb169', 'Yb170', 'Yb171', 'Yb172',
    'Yb173', 'Yb174', 'Yb175', 'Yb176', 'Zn64', 'Zn65',
    'Zn66', 'Zn67', 'Zn68', 'Zn69', 'Zn70', 'Zr88',
    'Zr89', 'Zr90', 'Zr91', 'Zr92', 'Zr93', 'Zr94',
    'Zr95', 'Zr96'
]

tendl_2019_base_url = 'https://github.com/openmc-data-storage/TENDL-2019/raw/main/h5_files/'

tendl_2019_xs_info = []
for isotope in tendl_2019_isotopes:
    entry = {}
    entry['isotope'] = isotope
    entry['library'] = 'TENDL-2019'
    entry['remote_file'] = entry['isotope'] + '.h5'
    entry['url'] = tendl_2019_base_url + entry['remote_file']
    entry['element'] = re.split('(\d+)', entry['isotope'])[0]
    entry['local_file'] = entry['library'] + '_' + entry['remote_file']
    tendl_2019_xs_info.append(entry)
    # could add size of file in mb as well


endfb_71_nndc_isotopes = [
    'Ac225', 'Ac226', 'Ac227', 'Ag107', 'Ag109', 'Ag110_m1', 'Ag111', 'Al27',
    'Am240', 'Am241', 'Am242', 'Am242_m1', 'Am243', 'Am244', 'Am244_m1',
    'Ar36', 'Ar38', 'Ar40', 'As74', 'As75', 'Au197', 'B10', 'B11', 'Ba130',
    'Ba132', 'Ba133', 'Ba134', 'Ba135', 'Ba136', 'Ba137', 'Ba138', 'Ba140',
    'Be7', 'Be9', 'Bi209', 'Bk245', 'Bk246', 'Bk247', 'Bk248', 'Bk249',
    'Bk250', 'Br79', 'Br81', 'C0', 'Ca40', 'Ca42', 'Ca43', 'Ca44', 'Ca46',
    'Ca48', 'Cd106', 'Cd108', 'Cd110', 'Cd111',
    'Cd112', 'Cd113', 'Cd114', 'Cd115_m1', 'Cd116', 'Ce136', 'Ce138', 'Ce139',
    'Ce140', 'Ce141', 'Ce142', 'Ce143', 'Ce144', 'Cf246', 'Cf248', 'Cf249',
    'Cf250', 'Cf251', 'Cf252', 'Cf253', 'Cf254', 'Cl35', 'Cl37', 'Cm240',
    'Cm241', 'Cm242', 'Cm243', 'Cm244', 'Cm245', 'Cm246', 'Cm247', 'Cm248',
    'Cm249', 'Cm250', 'Co58', 'Co58_m1', 'Co59', 'Cr50', 'Cr52', 'Cr53',
    'Cr54', 'Cs133', 'Cs134', 'Cs135', 'Cs136', 'Cs137', 'Cu63', 'Cu65',
    'Dy156', 'Dy158', 'Dy160', 'Dy161', 'Dy162', 'Dy163', 'Dy164', 'Er162',
    'Er164', 'Er166', 'Er167', 'Er168', 'Er170', 'Es251', 'Es252', 'Es253',
    'Es254', 'Es254_m1', 'Es255', 'Eu151', 'Eu152', 'Eu153', 'Eu154', 'Eu155',
    'Eu156', 'Eu157', 'F19', 'Fe54', 'Fe56', 'Fe57', 'Fe58', 'Fm255', 'Ga69',
    'Ga71', 'Gd152', 'Gd153', 'Gd154', 'Gd155', 'Gd156', 'Gd157', 'Gd158',
    'Gd160', 'Ge70', 'Ge72', 'Ge73', 'Ge74', 'Ge76', 'H1', 'H2', 'H3', 'He3',
    'He4', 'Hf174', 'Hf176', 'Hf177', 'Hf178', 'Hf179', 'Hf180', 'Hg196',
    'Hg198', 'Hg199', 'Hg200', 'Hg201', 'Hg202', 'Hg204', 'Ho165', 'Ho166_m1',
    'I127', 'I129', 'I130', 'I131', 'I135', 'In113', 'In115', 'Ir191', 'Ir193',
    'K39', 'K40', 'K41', 'Kr78', 'Kr80', 'Kr82', 'Kr83', 'Kr84', 'Kr85',
    'Kr86', 'La138', 'La139', 'La140', 'Li6', 'Li7', 'Lu175', 'Lu176', 'Mg24',
    'Mg25', 'Mg26', 'Mn55', 'Mo100', 'Mo92', 'Mo94', 'Mo95', 'Mo96', 'Mo97',
    'Mo98', 'Mo99', 'N14', 'N15', 'Na22', 'Na23', 'Nb93', 'Nb94', 'Nb95',
    'Nd142', 'Nd143', 'Nd144', 'Nd145', 'Nd146', 'Nd147', 'Nd148', 'Nd150',
    'Ni58', 'Ni59', 'Ni60', 'Ni61', 'Ni62', 'Ni64', 'Np234', 'Np235', 'Np236',
    'Np237', 'Np238', 'Np239', 'O16', 'O17', 'P31', 'Pa229', 'Pa230', 'Pa231',
    'Pa232', 'Pa233', 'Pb204', 'Pb206', 'Pb207', 'Pb208', 'Pd102', 'Pd104',
    'Pd105', 'Pd106', 'Pd107', 'Pd108', 'Pd110', 'Pm147', 'Pm148', 'Pm148_m1',
    'Pm149', 'Pm151', 'Pr141', 'Pr142', 'Pr143', 'Pu236', 'Pu237', 'Pu238',
    'Pu239', 'Pu240', 'Pu241', 'Pu242', 'Pu243', 'Pu244', 'Pu246', 'Ra223',
    'Ra224', 'Ra225', 'Ra226', 'Rb85', 'Rb86', 'Rb87', 'Re185', 'Re187',
    'Rh103', 'Rh105', 'Ru100', 'Ru101', 'Ru102', 'Ru103', 'Ru104', 'Ru105',
    'Ru106', 'Ru96', 'Ru98', 'Ru99', 'S32', 'S33', 'S34', 'S36', 'Sb121',
    'Sb123', 'Sb124', 'Sb125', 'Sb126', 'Sc45', 'Se74', 'Se76', 'Se77',
    'Se78', 'Se79', 'Se80', 'Se82', 'Si28', 'Si29', 'Si30', 'Sm144', 'Sm147',
    'Sm148', 'Sm149', 'Sm150', 'Sm151', 'Sm152', 'Sm153', 'Sm154', 'Sn112',
    'Sn113', 'Sn114', 'Sn115', 'Sn116', 'Sn117', 'Sn118', 'Sn119', 'Sn120',
    'Sn122', 'Sn123', 'Sn124', 'Sn125', 'Sn126', 'Sr84', 'Sr86', 'Sr87',
    'Sr88', 'Sr89', 'Sr90', 'Ta180', 'Ta181', 'Ta182', 'Tb159', 'Tb160',
    'Tc99', 'Te120', 'Te122', 'Te123', 'Te124', 'Te125', 'Te126', 'Te127_m1',
    'Te128', 'Te129_m1', 'Te130', 'Te132', 'Th227', 'Th228', 'Th229', 'Th230',
    'Th231', 'Th232', 'Th233', 'Th234', 'Ti46', 'Ti47', 'Ti48', 'Ti49', 'Ti50',
    'Tl203', 'Tl205', 'Tm168', 'Tm169', 'Tm170', 'U230', 'U231', 'U232',
    'U233', 'U234', 'U235', 'U236', 'U237', 'U238', 'U239', 'U240', 'U241',
    'V50', 'V51', 'W180', 'W182', 'W183', 'W184', 'W186', 'Xe123', 'Xe124',
    'Xe126', 'Xe128', 'Xe129', 'Xe130', 'Xe131', 'Xe132', 'Xe133', 'Xe134',
    'Xe135', 'Xe136', 'Y89', 'Y90', 'Y91', 'Zn64', 'Zn65', 'Zn66', 'Zn67',
    'Zn68', 'Zn70', 'Zr90', 'Zr91', 'Zr92', 'Zr93', 'Zr94', 'Zr95', 'Zr96'
]

endfb_71_nndc_base_url = 'https://github.com/openmc-data-storage/ENDF-B-VII.1-NNDC/raw/main/h5_files/neutron/'

endfb_71_nndc_xs_info = []
for isotope in endfb_71_nndc_isotopes:
    entry = {}
    entry['isotope'] = isotope
    entry['library'] = 'ENDFB-7.1-NNDC'
    entry['remote_file'] = entry['isotope'] + '.h5'
    entry['url'] = endfb_71_nndc_base_url + entry['remote_file']
    entry['element'] = re.split('(\d+)', entry['isotope'])[0]
    entry['local_file'] = entry['library'] + '_' + entry['remote_file']
    endfb_71_nndc_xs_info.append(entry)
    # could add size of file in mb as well


fendl_31d_isotopes = [
    'Ag107', 'Ag109', 'Al27', 'Ar36', 'Ar38', 'Ar40', 'Au197', 'B10', 'B11',
    'Ba130', 'Ba132', 'Ba134', 'Ba135', 'Ba136', 'Ba137', 'Ba138', 'Be9',
    'Bi209', 'Br79', 'Br81', 'C12', 'C13', 'Ca40', 'Ca42', 'Ca43', 'Ca44',
    'Ca46', 'Ca48', 'Cd106', 'Cd108', 'Cd110', 'Cd111', 'Cd112', 'Cd113',
    'Cd114', 'Cd116', 'Ce136', 'Ce138', 'Ce140', 'Ce142', 'Cl35', 'Cl37',
    'Co59', 'Cr50', 'Cr52', 'Cr53', 'Cr54', 'Cs133', 'Cu63',
    'Cu65', 'Er162', 'Er164', 'Er166', 'Er167', 'Er168',
    'Er170', 'F19', 'Fe54', 'Fe56', 'Fe57', 'Fe58',
    'Ga69', 'Ga71', 'Gd152', 'Gd154', 'Gd155', 'Gd156',
    'Gd157', 'Gd158', 'Gd160', 'Ge70', 'Ge72', 'Ge73',
    'Ge74', 'Ge76', 'H1', 'H2', 'H3', 'He3', 'He4',
    'Hf174', 'Hf176', 'Hf177', 'Hf178', 'Hf179', 'Hf180',
    'I127', 'K39', 'K40', 'K41', 'La138', 'La139', 'Li6',
    'Li7', 'Lu175', 'Lu176', 'Mg24', 'Mg25', 'Mg26',
    'Mn55', 'Mo100', 'Mo92', 'Mo94', 'Mo95', 'Mo96',
    'Mo97', 'Mo98', 'N14', 'N15', 'Na23', 'Nb93', 'Ni58',
    'Ni60', 'Ni61', 'Ni62', 'Ni64', 'O16', 'O17', 'O18',
    'P31', 'Pb204', 'Pb206', 'Pb207', 'Pb208', 'Pt190',
    'Pt192', 'Pt194', 'Pt195', 'Pt196', 'Pt198', 'Re185',
    'Re187', 'Rh103', 'S32', 'S33', 'S34', 'S36', 'Sb121',
    'Sb123', 'Sc45', 'Si28', 'Si29', 'Si30', 'Sn112',
    'Sn114', 'Sn115', 'Sn116', 'Sn117', 'Sn118', 'Sn119',
    'Sn120', 'Sn122', 'Sn124', 'Ta181', 'Th232', 'Ti46',
    'Ti47', 'Ti48', 'Ti49', 'Ti50', 'U235', 'U238', 'V50',
    'V51', 'W180', 'W182', 'W183', 'W184', 'W186', 'Y89',
    'Zn64', 'Zn66', 'Zn67', 'Zn68', 'Zn70', 'Zr90',
    'Zr91', 'Zr92', 'Zr94', 'Zr96',
]

fendl_31d_base_url = 'https://github.com/openmc-data-storage/FENDL-3.1d/raw/main/h5_files/neutron/'

fendl_31d_xs_info = []
for isotope in fendl_31d_isotopes:
    entry = {}
    entry['isotope'] = isotope
    entry['library'] = 'FENDL-3.1d'
    entry['remote_file'] = entry['isotope'] + '.h5'
    entry['url'] = fendl_31d_base_url + entry['remote_file']
    entry['element'] = re.split('(\d+)', entry['isotope'])[0]
    entry['local_file'] = entry['library'] + '_' + entry['remote_file']
    fendl_31d_xs_info.append(entry)
    # could add size of file in mb as well

xs_info = endfb_71_nndc_xs_info + tendl_2019_xs_info + fendl_31d_xs_info

all_libs = []
for entry in xs_info:
    all_libs.append(entry['library'])

LIB_OPTIONS = list(set(all_libs))
