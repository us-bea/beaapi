# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.1.0
### Added
- Add some general SBOM info in `conda.txt`
- Switch to using new package_template format
- Include some extra metadata on release dates of estimates
- Allow forcing some parameter combinations that may cause a problem
- Improved throttling prediction
- Add note for `get_data` not yet handling `APIDatasetMetaData`
### Fixed
- Fix throttling bug where last query was over max data rate limit
- Accommodate the new `IntlServSTA` dataset
- Fix bug where I wasn't reraising caught (but unhandled) error
- Fix bug when moving from pandas 1.5.3 to 2.2.2 with milliseconds in datetime
### Changed
- Force DataValue to be a `float64`/`int64` type, even if newer pandas versions tries to convert to `Float64`/`Int64` extension types.

## 0.0.2
### Added
- Provide means to automatically throttle calls
- Provide meta-data on data columns for reshaping as well as experimental `to_wide_vars_in_cols()` and `to_wide_vars_in_rows()`
- Provide some basic Error subtypes.
- Handle API failures better (both empty and HTML message responses)
- Print message if non-standard `get_data()` parameters are provided as those will be dropped.

### Fixed
- Do a better job of converting numbers to strings in DataValue
