# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.0.2
### Added
- Provide means to automatically throttle calls
- Provide meta-data on data columns for reshaping as well as experimental `to_wide_vars_in_cols()` and `to_wide_vars_in_rows()`
- Provide some basic Error subtypes.
- Handle API failures better (both empty and HTML message responses)
- Print message if non-standard `get_data()` parameters are provided as those will be dropped.

### Fixed
- Do a better job of converting numbers to strings in DataValue
