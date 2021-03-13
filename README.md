
[![CI - Main](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/docker_ci_main.yml/badge.svg)](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/docker_ci_main.yml)
[![Upload Python Package](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/python-publish.yml/badge.svg)](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/python-publish.yml)
[![PyPI](https://img.shields.io/pypi/v/openmc_data_downloader?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/openmc_data_downloader/)

# OpenMC data downloader

A Python package for downloading preprocessed cross section data in the h5 file
format for use with OpenMC.

This package allows you to download a fully reproducable composite nuclear data
library with one command.

There are several methods of obtaining complete data libraries for use with
OpenMC, for example:

- [OpenMC.org](https://openmc.org/) has entrie libraries downloadable as compressed files
- [OpenMC data repository scripts](https://github.com/openmc-dev/data/) has scripts for automatically downloading ACE and ENDF files and generating h5 files from these inputs.


## History

The package was originally conceived by Jonathan Shimwell as a means of
downloading a minimal selection of data for use on continious intergration
platforms.
The package can also used to produce traceable and reproducable
nuclear data distributions.

## System Installation

To install the openmc_data_downloader you need to have Python3 installed,
OpenMC is also advisable if you want to run simulations using the h5 data files
but not actually madatory if you just want to download the cross sections.


```bash
pip install openmc_data_downloader
```

## Features

The OpenMC data downloader is able to download corss section files for isotopes
from nuclear data libraries.The user specifies the nuclear data libraries in
order of their preference. When an isotope is found in multiple libraries it
will be downloaded from the highest preference library. This avoid duplication
of isotopes and provides a reproductible nuclear data enviroment.

The nuclear data h5 file are downloaded from the OpenMC-data-storage
repository. Prior to being added to the repository they have been automatically
processed using scripts from OpenMC data repository, these scripts convert ACE
and ENDF file to h5 files.

The resulting h5 files are then used in and automated test suite of simulations
to help ensure they are suitable for their intended purpose.

Isotopes for downloading can be found in a varity of ways as demonstrated below.
When downloading a cross_section.xml file is automatically created and h5 files
are named with their nuclear data library and the isotope. This helps avoid
redownloading files that already exist locally.

## Usage - command line usage

### Getting a description of the input options
```bash
openmc_data_downloader --help
```

### Downloading a single isotope from the TENDL 2019 nuclear library
```bash
openmc_data_downloader -l TENDL_2019 -i Li6
```

### Downloading a multiple isotopes from the TENDL 2019 nuclear library
```bash
openmc_data_downloader -l TENDL_2019 -i Li6 Li7
```

### Downloading a single element from the TENDL 2019 nuclear library
```bash
openmc_data_downloader -l TENDL_2019 -e Li
```

### Downloading a multiple element from the TENDL 2019 nuclear library
```bash
openmc_data_downloader -l TENDL_2019 -e Li Si Na
```
### Downloading h5 files from the ENDF/B 7.1 NNDC library to a specific folder (destination)
```bash
openmc_data_downloader -l ENDFB_71_NNDC -i Be9 -d my_h5_files
```

### Downloading a combination of isotopes and element from the TENDL 2019 nuclear library
```bash
openmc_data_downloader -l TENDL_2019 -e Li Si Na -i Fe56 U235
```

### Downloading all the isotopes in a materials.xml file from the TENDL 2019 nuclear library
```bash
openmc_data_downloader -l TENDL_2019 -m materials.xml
```

### Downloading 3 isotopes from ENDF/B 7.1 NNDC (first choice) and TENDL 2019 (second choice) nuclear library
```bash
openmc_data_downloader -l TENDL_2019 ENDFB_71_NNDC -i Li6 Li7 Be9
```

### Downloading an isotopes from ENDF/B 7.1 NNDC and setting the OPENMC_CROSS_SECTION enviromental varible to 
```bash
openmc_data_downloader -l TENDL_2019 ENDFB_71_NNDC -i Li6 Li7 Be9
```

## Usage - within a Python enviroment

When using the Python API the ```just_in_time_library_generator()``` function
provides similar capabilities to the ```openmc_data_downloader``` terminal
command. With one key difference being that ```just_in_time_library_generator()```
sets the ```OPENMC_CROSS_SECTIONS``` enviromental varible to point to the
newly created cross_sections.xml by default.

### Downloading the isotopes present in an OpenMC material
```python
import openmc
import openmc_data_downloader as odd

mat1 = openmc.Material()
mat1.add_element('Fe', 0.95)
mat1.add_element('C', 0.05)

odd.just_in_time_library_generator(
    libraries='TENDL_2019',
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
    libraries=['ENDFB_71_NNDC', 'TENDL_2019'],
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

odd.just_in_time_library_generator(
    libraries='ENDFB_71_NNDC',
    materials=[mat1, mat2]
)
```

### Downloading some isotopes and elements from the TENDL 2019 library
```python
import openmc
import openmc_data_downloader as odd

odd.just_in_time_library_generator(
    libraries='TENDL_2019',
    elements=['Li', 'Be'],
    isotopes=['Fe56', 'U235'],
)
```
