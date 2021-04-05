
FROM openmc/openmc:develop


COPY openmc_data_downloader openmc_data_downloader/
COPY setup.py setup.py
COPY tests tests/
COPY README.md README.md

RUN python setup.py develop

CMD pytest tests -v --cov=openmc_data_downloader --cov-report term --cov-report xml ; mv coverage.xml /share/coverage.xml
