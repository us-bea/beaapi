from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'BEA API Python package'
LONG_DESCRIPTION = 'A package for accessing the BEA API from Python and returning data as a NumPy array, unformatted JSON, unformatted XML, or, optionally, as a Pandas DataFrame.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="beaapi", 
        version=VERSION,
        author="Andrea Batch, Brian Quistorff",
        author_email="<developers@bea.gov>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas'], #, 'fuzzywuzzy' (comment out for now while in flux)
        keywords=['python', 'bea api', 'bureau of economic analysis', 'economic data'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Intended Audience :: Financial and Insurance Industry",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)