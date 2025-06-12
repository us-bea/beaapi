"""
This is a place to provide a slightly longer package description.
"""

# Provides a version number from your Git repositry, Git tags--DO NOT REMOVE
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("beaapi")
except PackageNotFoundError:
    __version__ = "unknown version"

# Include any code that should get run when the package is imported here
# Common examples of code to place here include:
#    * Defining important constants
#    * Importing functionality from modules that you don't want your user to need to separately import

__all__ = ['api_request', 'get_data', 'get_data_set_list', 'get_parameter_list',
           'get_parameter_values', 'update_metadata', 'search_metadata',
           'get_parameter_values_filtered', 'to_wide_vars_in_cols',
           'to_wide_vars_in_rows', 'ThrottlingCaller', 'BEAAPIError', 'BEAAPIFailure',
           'BEAAPIResponseError', 'BEAAPIPkgException']
from .beaapi_error import BEAAPIError, BEAAPIFailure, BEAAPIResponseError, BEAAPIPkgException
from .api_request import api_request
from .get_data import get_data, to_wide_vars_in_cols, to_wide_vars_in_rows
from .get_data_set_list import get_data_set_list
from .get_parameter_list import get_parameter_list
from .get_parameter_values import get_parameter_values
from .get_parameter_values_filtered import get_parameter_values_filtered
from .update_metadata import update_metadata
from .search_metadata import search_metadata
from .throttling_caller import ThrottlingCaller

#: Max lenght of API responses per minute before throttling happens
MAX_DATA_PER_MINUTE = 100 * 1000 * 1024

#: Max number of API requests per minute before throttling happens
MAX_REQUESTS_PER_MINUTE = 100

#: Max number of API errors per minute before throttling happens
MAX_ERRORS_PER_MINUTE = 30

#: Max number of API requests per minute before throttling happens
BACKOFF_SECS = 60 * 60
