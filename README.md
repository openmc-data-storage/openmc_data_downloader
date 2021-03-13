
[![CI - Main](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/docker_ci_main.yml/badge.svg)](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/docker_ci_main.yml)
[![Upload Python Package](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/python-publish.yml/badge.svg)](https://github.com/openmc-data-storage/openmc_data_downloader/actions/workflows/python-publish.yml)
[![PyPI](https://img.shields.io/pypi/v/openmc_data_downloader?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/openmc_data_downloader/)

# OpenMC data downloader

A Python package for downloading preprocessed cross section data in the h5 file
format for use with OpenMC.

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

#TODO
## Usage - command line usage

#TODO

## Usage - within a Python enviroment
#TODO