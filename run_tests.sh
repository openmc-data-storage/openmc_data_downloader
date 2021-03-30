#!/bin/bash

pytest tests -v --cov=openmc_data_downloader --cov-report term --cov-report xml
