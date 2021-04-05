
FROM openmc/openmc:develop

RUN apt-get install -y curl

COPY openmc_data_downloader openmc_data_downloader/
COPY run_tests.sh run_tests.sh
COPY setup.py setup.py
COPY tests tests/
COPY README.md README.md

RUN python setup.py develop

CMD pytest tests -v --cov=openmc_data_downloader --cov-report term --cov-report xml ; bash <(curl -s https://codecov.io/env)

