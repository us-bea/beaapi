# Contributing
A big welcome and thank you for considering contributing to BEA open source projects! It’s people like you that make it a reality for users in our community.

Reading and following these guidelines will help us make the contribution process easy and effective for everyone involved. It also communicates that you agree to respect the time of the developers managing and developing these open source projects. In return, we will reciprocate that respect by addressing your issue, assessing changes, and helping you finalize your pull requests.

## Code of Conduct

We take our open source community seriously and hold ourselves and other contributors to high standards of communication. By participating and contributing to this project, you agree to uphold our [Code of Conduct](https://github.com/us-bea/.github/blob/main/CODE_OF_CONDUCT.md).

## Getting Started

Contributions are made to this repo via Issues and Pull Requests (PRs). A few general guidelines that cover both:

- To report security vulnerabilities, please see [SECURITY](https://github.com/us-bea/beaapi/security/policy).
- Search for existing Issues and PRs before creating your own.
- We work hard to makes sure issues are handled in a timely manner but, depending on the impact, it could take a while to investigate the root cause. A friendly ping in the comment thread to the submitter or a contributor can help draw attention if your issue is blocking.

## Issues
Issues should be used to report problems with the library, request a new feature, or to discuss potential changes before a PR is created. When you create a new Issue, a template will be loaded that will guide you through collecting and providing the information we need to investigate.

If you find an Issue that addresses the problem you're having, please add your own reproduction information to the existing issue rather than creating a new one. Adding a reaction can also help be indicating to our maintainers that a particular problem is affecting more than just the reporter.

## Pull Requests
PRs to our libraries are always welcome and can be a quick way to get your fix or improvement slated for the next release. In general, PRs should:

- Only fix/add the functionality in question OR address wide-spread whitespace/style issues, not both.
- Add unit or integration tests for fixed or changed functionality (if a test suite already exists).
- Address a single concern in the least number of changed lines as possible.
- Include documentation in the repo or on our docs site.
- Be accompanied by a complete Pull Request template (loaded automatically when a PR is created).

For changes that address core functionality or would require breaking changes (e.g. a major release), it's best to open an Issue to discuss your proposal first. This is not required but can save time creating and reviewing changes.


## Development


### To Build and install the development version of the bea Python Library
To build, you must have the `build` package (`python-build` for Anaconda). Then clone this repository, and switch to the repo directory. Then, you must build and install the wheel. 

To generate the distribution packages with `build` (and `setuptools` and `wheel`):
```
python -m build --no-isolation
```
(`--no-isolation` may not be needed if your virtual environment can install `setuptools` via PyPI.)

Then, install from the wheel file (fill in version):
```
python -m pip install --upgrade --force-reinstall dist/beaapi-X.Y.Z-py3-none-any.whl
```

An alternative to installing the wheel is to install this package in "development mode" for Anaconda:
```
conda develop .
```

### Building docs
All takes place `docsrc/`. To build `README.md` from `README.ipynb` you will need `jupyter`, `python-dotenv`, and `nbconvert` (6.4.4 has error, 7.2.9 works)
```
jupyter nbconvert --to markdown README.ipynb --output "../README.md"
```

To build the docs you will need `sphinx`, `nbsphinx`, `pandoc` and `nbconvert`. Then:

```
make html
```
which will generate html docs viewable at `doc/index.html`. 

You can remove `*.ipynb`s from `../docs`.
```CMD
del ..\docs\*.ipynb
```


### Testing
To run just a a quick-test
```
pytest tests/
```

Optional (non-default) tests can be run with:
```
pytest tests/throttling.py
```

Or `coverage run -m pytest tests/` to run with coverage. And then `coverage report` to see summary stats or `coverage html` to generate an HTML report in `htmlcov/index.html`.

Try to run the tests in the latest version of pandas.

### Linting
We use the `flake8` and `mypy` package to check for style errors. (To fully use `mypy` you will also need to install the `pandas-stubs` package.)
```
flake8 beaapi/
mypy beaapi/
```
`mypy` might complain about fuzzywuzzy which is OK


