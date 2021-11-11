import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openmc_data_downloader",
    version="develop",
    summary="Download cross section h5 files for use in OpenMC",
    author="Jonathan Shimwell",
    author_email="mail@jshimwell.com",
    description="A tool for selectively downloading h5 files for specified isotopes / elements from your libraries of choice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openmc-data-storage/openmc_data_downloader",
    packages=setuptools.find_packages(),
    zip_safe=True,
    package_dir={"openmc_data_downloader": "openmc_data_downloader"},
    scripts=["openmc_data_downloader/openmc_data_downloader"],
    package_data={
        "openmc_data_downloader": [
            "requirements.txt",
            "README.md",
            "LICENSE",
        ]
    },
    classifiers=[
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    tests_require=["pytest-cov", "pytest-runner"],
    install_requires=[
        "pandas",
        # 'openmc' is optional for this package but is not available via pip install at the moment
    ],
)
