
[![CI - Main](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/docker_ci_main.yml/badge.svg)](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/docker_ci_main.yml)
[![Upload Python Package](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/python-publish.yml/badge.svg)](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/python-publish.yml)
[![PyPI](https://img.shields.io/pypi/v/openmc_data_downloader?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/openmc_data_downloader/)
[![codecov](https://codecov.io/gh/openmc-data-storage/openmc_data_downloader/branch/main/graph/badge.svg)](https://codecov.io/gh/openmc-data-storage/openmc_data_downloader)

# OpenMC data downloader

A Python package for downloading preprocessed cross section data in the h5 file
format for use with OpenMC.

This package allows you to download a fully reproducible composite nuclear data
library with one command.

There are several methods of obtaining complete data libraries for use with
OpenMC, for example:

- [OpenMC.org](https://openmc.org/) has entire libraries downloadable as compressed files
- [OpenMC data repository scripts](https://github.com/openmc-dev/data/) has scripts for automatically downloading ACE and ENDF files and generating h5 files from these inputs.

## History

The package was originally conceived by Jonathan Shimwell as a means of
downloading a minimal selection of data for use on continuous integration
platforms.
The package can also used to produce traceable and reproducible
nuclear data distributions.

## System Installation

To install the openmc_data_downloader you need to have Python3 installed,
OpenMC is also advisable if you want to run simulations using the h5 data files
but not actually mandatory if you just want to download the cross sections.

```bash
pip install openmc_data_downloader
```

## Features

The OpenMC data downloader is able to download cross section files for isotopes
from nuclear data libraries.The user specifies the nuclear data libraries in
order of their preference. When an isotope is found in multiple libraries it
will be downloaded from the highest preference library. This avoid duplication
of isotopes and provides a reproducible nuclear data environment.

The nuclear data h5 file are downloaded from the OpenMC-data-storage
repository. Prior to being added to the repository they have been automatically
processed using scripts from OpenMC data repository, these scripts convert ACE
and ENDF file to h5 files.

The resulting h5 files are then used in and automated test suite of simulations
to help ensure they are suitable for their intended purpose.

Isotopes for downloading can be found in a variety of ways as demonstrated below.
When downloading a cross_section.xml file is automatically created and h5 files
are named with their nuclear data library and the isotope. This helps avoid
downloading files that already exist locally and the ```overwrite``` argument
can be used to control if these files are downloaded again.

## Usage - command line usage

### Getting a description of the input options

```bash
openmc_data_downloader --help
```

### Downloading a single isotope from the FENDL 3.1d nuclear library

```bash
openmc_data_downloader -l FENDL-3.1d -i Li6
```

### Downloading a multiple isotopes from the TENDL 2019 nuclear library

```bash
openmc_data_downloader -l TENDL-2019 -i Li6 Li7
```

### Downloading a single element from the TENDL 2019 nuclear library

```bash
openmc_data_downloader -l TENDL-2019 -e Li
```

### Downloading a multiple element from the TENDL 2019 nuclear library

```bash
openmc_data_downloader -l TENDL-2019 -e Li Si Na
```

### Downloading h5 files from the ENDF/B 7.1 NNDC library to a specific folder (destination)

```bash
openmc_data_downloader -l ENDFB-7.1-NNDC -i Be9 -d my_h5_files
```

### Downloading a combination of isotopes and element from the TENDL 2019 nuclear library

```bash
openmc_data_downloader -l TENDL-2019 -e Li Si Na -i Fe56 U235
```
### Downloading all the isotopes from the TENDL 2019 nuclear library

```bash
openmc_data_downloader -l TENDL-2019 -i all
```
### Downloading all the stable isotopes from the TENDL 2019 nuclear library

```bash
openmc_data_downloader -l TENDL-2019 -i stable
```

### Downloading all the isotopes in a materials.xml file from the TENDL 2019 nuclear library

```bash
openmc_data_downloader -l TENDL-2019 -m materials.xml
```

### Downloading 3 isotopes from ENDF/B 7.1 NNDC (first choice) and TENDL 2019 (second choice) nuclear library

```bash
openmc_data_downloader -l ENDFB-7.1-NNDC TENDL-2019 -i Li6 Li7 Be9
```

### Downloading the photon only cross section for an element ENDF/B 7.1 NNDC

```bash
openmc_data_downloader -l ENDFB-7.1-NNDC -e Li -p photon 
```

### Downloading the neutron and photon cross section for an element ENDF/B 7.1 NNDC

```bash
openmc_data_downloader -l ENDFB-7.1-NNDC -e Li -p neutron photon
```

### Downloading the neutron cross section for elements and an SaB cross sections

```bash
openmc_data_downloader -l ENDFB-7.1-NNDC -e Be O -s c_Be_in_BeO
```

## Usage - within a Python environment

When using the Python API the ```just_in_time_library_generator()``` function
provides similar capabilities to the ```openmc_data_downloader``` terminal
command. With one key difference being that ```just_in_time_library_generator()```
sets the ```OPENMC_CROSS_SECTIONS``` environmental variable to point to the
newly created cross_sections.xml by default.

### Downloading the isotopes present in an OpenMC material

```python
import openmc
import openmc_data_downloader as odd

mat1 = openmc.Material()
mat1.add_element('Fe', 0.95)
mat1.add_element('C', 0.05)

odd.just_in_time_library_generator(
    libraries='FENDL-3.1d',
    materials=mat1
)
```

### Downloading the isotopes present in an OpenMC material from two libraries but with a preference for ENDF/B 7.1 NNDC library over TENDL 2019

```python
import openmc
import openmc_data_downloader as odd

mat1 = openmc.Material()
mat1.add_element('Fe', 0.95)
mat1.add_element('C', 0.05)

odd.just_in_time_library_generator(
    libraries=['ENDFB-7.1-NNDC', 'TENDL-2019'],
    materials=mat1
)
```

### Downloading the isotopes in several OpenMC materials

```python
import openmc
import openmc_data_downloader as odd

mat1 = openmc.Material()
mat1.add_element('Fe', 0.95)
mat1.add_element('C', 0.05)

mat2 = openmc.Material()
mat2.add_element('H', 0.66)
mat2.add_element('0', 0.33)

# a list of openmc.Material objects can be used
odd.just_in_time_library_generator(
    libraries='ENDFB-7.1-NNDC',
    materials=[mat1, mat2]
)

# alternatively an openmc.Materials() object can be used
mats = openmc.Materials([mat1, mat2]) 
odd.just_in_time_library_generator(
    libraries='ENDFB-7.1-NNDC',
    materials=mats
)
```

### Downloading neutron cross sections for a material with an SaB

```python
import openmc
import openmc_data_downloader as odd

my_mat = openmc.Material()
my_mat.add_element('Be', 0.5)
my_mat.add_element('O', 0.5)
my_mat.add_s_alpha_beta('Be_in_BeO')

odd.just_in_time_library_generator(
    libraries='ENDFB-7.1-NNDC',
    materials= my_mat
    particles = ['neutron'],
)
```

### Downloading photon and neutron cross sections for isotopes and elements from the TENDL 2019 library

```python
import openmc
import openmc_data_downloader as odd

odd.just_in_time_library_generator(
    libraries='TENDL-2019',
    elements=['Li', 'Be'],
    particles = ['photon', 'neutron'],
    isotopes=['Fe56', 'U235'],
)
```
