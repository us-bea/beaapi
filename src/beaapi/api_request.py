from dataclasses import dataclass
import math

# import urllib.request
# import urllib.parse
import requests
from typing import Union, Dict, List
#import pandas as pd
from throttling_caller import throttling_data, ThrottlingCaller

# from .beaapi_error import BEAAPIFailure, BEAAPIResponseError


class BeaApiParams:
    """Enumeration of BEA API parameters"""

    @dataclass(frozen=True)
    class RequestMethods:
        """Enumeration of BEA API methods"""

        GET_DATA = {"method": "GetData"}
        GET_DATA_SET_LIST = {"method": "GetDataSetList"}
        GET_PARAMETER_LIST = {"method": "GetParameterList"}
        GET_PARAMETER_VALUES = {"method": "GetParameterValues"}
        GET_PARAMETER_VALUES_FILTERED = {"method": "GetParameterValuesFiltered"}
        GET_PARAMETER_VALUES_FILTERED_FOR_TEXT = {
            "method": "GetParameterValuesFilteredForText"
        }
        GET_PARAMETER_VALUES_TEXT = {"method": "GetParameterValuesText"}
        GET_REGIONAL_DATA = {"method": "GetRegionalData"}
        GET_USER_ID = {"method": "GetUserID"}
        GET_USER_ID_LIST = {"method": "GetUserIDList"}

    @dataclass(frozen=True)
    class ResultFormats:
        """Enumeration of BEA API result formats"""

        JSON = {"ResultFormat": "json"}
        XML = {"ResultFormat": "xml"}

    @dataclass(frozen=True)
    class Frequency:
        """Enumeration of BEA API frequencies"""

        ANNUAL = {"frequency": "A"}
        QUARTERLY = {"frequency": "Q"}
        MONTHLY = {"frequency": "M"}

    @dataclass(frozen=True)
    class ParameterName:
        TABLE_ID = {"parametername": "TableID"}


class ApiRequest:
    BASE_URI = "https://apps.bea.gov/api/data/"

    def __init__(
        self,
        user_id: str,
        method: BeaApiParams.RequestMethods,
        result_format: BeaApiParams.ResultFormats,
        throttle: bool = True,
    ):
        self._required_params_ = {"UserID": user_id}
        for i in [method, result_format]:
            self._required_params_.update(i)
        if user_id not in throttling_data:
          throttling_data[user_id] = ThrottlingCaller()
    
    def make_request(func: callable) -> requests.Response:
        """Makes the API request"""
        def wrappper(*args, **kwargs):
            data = func(*args, **kwargs)
            res = requests.get(ApiRequest.BASE_URI, params=data)
            res.raise_for_status()
            res.apparent_encoding
            return res.json().get("BEAAPI", {}).get("Results", {})
        return wrappper

    @make_request
    def get_data(
        self,
        frequency: Dict[str,Union[BeaApiParams.Frequency, str]] = None,
        datasetname: str = None,
        tablename: str = None,
        year: List[str] = None,
        **kwargs
    ) -> str:
        """Builds the request data for the API request"""

        new_params = {"datasetname": datasetname,
            "TableName" : tablename,
            "year": year,} 
        self._required_params_.update(frequency) if frequency is not None else None
        self._required_params_.update({k:v for k,v in new_params.items() if v is not None})
        return self._required_params_

if __name__ == "__main__":
    user_id = "ABB82901-7933-4E04-BDFB-2B906DDDB0ED"
    method = BeaApiParams.RequestMethods.GET_DATA
    result_format = BeaApiParams.ResultFormats.JSON
    api = ApiRequest(user_id, method, result_format)
    #print(api._required_params_)
    req = api.get_data(frequency=BeaApiParams.Frequency.ANNUAL, datasetname="NIPA", tablename="T20305", year=["2021"])
    print(req)





# def api_request(beaspec: Dict[str, str], as_string: bool = False, as_dict: bool = False,
#                 as_table: bool = True, is_meta: bool = False, throttle: bool = True,
#                 **kwargs: Dict[str, Any]) -> Union[http.client.HTTPResponse, str,
#                                                    Dict[str, Union[str,int]],
#                                                    pd.DataFrame]:
#     """
#     This is a low-level function (and subject to change). Please use the higher-level
#     ``get_*()`` functions!

#     Pass dict of user specifications (including API key) to return data from BEA API.

#     Parameters
#     ----------
#     beaspec :
#         A dict of user specifications (required). See the example below for general
#         idea. See BEA API documentation or use metadata methods for complete lists of
#         parameters.
#     as_string :
#         Return result body as a string. Supersedes ``as_dict`` and
#         ``as_table`` optional parameters.
#     as_dict :
#         Return response as ``json.loads('[response content]')`` dict.
#         Supersedes ``as_table`` optional parameter.
#     as_table :
#         Return response as ``pd.DataFrame`` with ``pd.DataFrame(...).attrs`` metadata
#     is_meta :
#         Is this a metadata request from ``get_data_set_list()``,
#         ``get_parameter_list()``, or ``get_parameter_values()``?
#         If so, data will be returned with only partial transformation

#     Returns
#     -------
#     http.client.HTTPResponse, str, dict, pd.DataFrame
#         The response from a query of BEA's API.
#         If ``as_string``, ``as_dict``, and ``as_table`` are all False, returns
#         ``http.client.HTTPResponse``.
#         If ``as_string=True``, returns string of response content.
#         If ``as_dict=True``, returns slightly transformed dict results of
#         ``json.loads()`` of response content.
#         If ``as_table``, An object of class ``pd.DataFrame`` containing data from
#         ``beaapi.api_request(...)`` with
#         metadata stored as an attribute in ``pd.DataFrame(...).attrs``.

#     Examples
#     --------
#     >>> import beaapi
#     >>> beaspecs = {
#     >>>     'UserID': beakey ,
#     >>>     'Method': 'GetData',
#     >>>     'datasetname': 'NIPA',
#     >>>     'TableName': 'T20305',
#     >>>     'Frequency': 'Q',
#     >>>     'Year': 'X',
#     >>> }
#     >>> beaPayload = beaapi.api_request(beaspecs)
#     """

#     encoding_str = 'iso-8859-1'  # 'utf-8' returns decode errors

#     if(not isinstance(beaspec, dict)):
#         print('Please specify API parameters as a list. For example: api_request('
#               '{"UserID": "YourKey", "Method": "GetData", [your remaining parameters]'
#               '))')
#         raise Exception('Invalid object class passed to api_request([list of API'
#                         ' parameters]): ' + str(type(beaspec)) + '. Should be of'
#                         ' class "dict"')

#     # Change spec names to lowercase and reassign
#     lower_beaspec = {k.lower(): v for k, v in beaspec.items()}
#     beaspec = lower_beaspec
#     # attributes(beaSpec)$names <- tolower(attributes(beaSpec)$names)

#     if(not isinstance(beaspec['userid'], str)):
#         raise Exception('Invalid API key of class ' + str(type(beaspec['userid'])))

#     beaspec['userid'] = beaspec['userid'].replace(' ', '')
#     beaspec['beaR'] = 'py_v1'

#     # Some defaults for user convenience
#     if not ('resultformat' in list(beaspec.keys())):
#         beaspec['resultformat'] = 'json'

#     if(len(beaspec['userid']) != 36):
#         raise Exception('Invalid API key: ' + beaspec['userid'])
#     # Parse user settings into API URL
#     params = urllib.parse.urlencode(beaspec)
#     bea_url = 'https://apps.bea.gov/api/data/?%s' % params

#     if throttle:
#         from .throttling_caller import throttling_data, ThrottlingCaller
#         userid = beaspec['userid']
#         if userid not in throttling_data:
#             throttling_data[userid] = ThrottlingCaller()

#         throttling_data[userid].wait_until_available()

#     # Make the API call and, for now, just return the response
#     with urllib.request.urlopen(bea_url) as f:
#         if(f.getcode() > 200):
#             raise Exception(f"Failed to retrieve data from {bea_url} with status code"
#                             " {f.getcode()}")
#         # beaPayload = f.read().decode(encoding_str)
#         bea_payload = f
#         # return(beaPayload)

#         try:
#             if(math.floor(bea_payload.status / 100) != 2):
#                 raise Exception('Request failed. Returned HTTP status code: '
#                                 + str(bea_payload['status_code']))
#         except Exception:
#             raise Exception('Submitted variable is not a valid https response class'
#                             ' object.')

#         # Give user format they want (do it in order of least modification unless
#         # nothing but as_table=False specified)
#         if(as_string):
#             bea_content = bea_payload.read().decode(encoding_str)
#             return(bea_content)
#         else:
#             if not as_dict and not as_table:
#                 return(bea_payload)

#             try:
#                 if (as_dict):
#                     from beaapi.response_to_dict import response_to_dict
#                     bea_response = response_to_dict(bea_payload, is_meta=is_meta)
#                     if throttle:
#                         rs = bea_response["response_size"]
#                         assert isinstance(rs, int)
#                         throttling_data[userid].log_query(rs)
#                     return(bea_response)
#                 else:  # as_table
#                     from beaapi.response_to_table import response_to_table
#                     bea_results = response_to_table(bea_payload)
#                     if throttle:
#                         td = throttling_data[userid]
#                         td.log_query(bea_results.attrs["response_size"])
#                     return(bea_results)
#             except BEAAPIFailure as e:
#                 if throttle:
#                     throttling_data[userid].wait_prev_failure = True
#                 raise e
#             except BEAAPIResponseError as e:
#                 if throttle:
#                     throttling_data[userid].log_query(e.response_size, True)
#                 raise e
