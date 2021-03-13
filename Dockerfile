
FROM openmc/openmc:develop

COPY openmc_data_downloader openmc_data_downloader/
COPY run_tests.sh run_tests.sh
COPY setup.py setup.py
COPY tests tests/
COPY README.md README.md

RUN python setup.py install
