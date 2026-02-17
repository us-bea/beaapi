import math
import urllib.request
import urllib.parse
from typing import Union, Any, Dict
import pandas as pd
import http
import beaapi

from .beaapi_error import BEAAPIFailure, BEAAPIResponseError

default_base_url = 'https://apps.bea.gov/api/data/?'
def api_request(beaspec: Dict[str, str], as_string: bool = False, as_dict: bool = False,
                as_table: bool = True, is_meta: bool = False, throttle: bool = True,
                **kwargs: Dict[str, Any]) -> Union[http.client.HTTPResponse, str,
                                                   Dict[str, Union[str,int]],
                                                   pd.DataFrame]:
    """
    This is a low-level function (and subject to change). Please use the higher-level
    ``get_*()`` functions!

    Pass dict of user specifications (including API key) to return data from BEA API.

    Parameters
    ----------
    beaspec :
        A dict of user specifications (required). See the example below for general
        idea. See BEA API documentation or use metadata methods for complete lists of
        parameters.
    as_string :
        Return result body as a string. Supersedes ``as_dict`` and
        ``as_table`` optional parameters.
    as_dict :
        Return response as ``json.loads('[response content]')`` dict.
        Supersedes ``as_table`` optional parameter.
    as_table :
        Return response as ``pd.DataFrame`` with ``pd.DataFrame(...).attrs`` metadata
    is_meta :
        Is this a metadata request from ``get_data_set_list()``,
        ``get_parameter_list()``, or ``get_parameter_values()``?
        If so, data will be returned with only partial transformation

    Returns
    -------
    http.client.HTTPResponse, str, dict, pd.DataFrame
        The response from a query of BEA's API.
        If ``as_string``, ``as_dict``, and ``as_table`` are all False, returns
        ``http.client.HTTPResponse``.
        If ``as_string=True``, returns string of response content.
        If ``as_dict=True``, returns slightly transformed dict results of
        ``json.loads()`` of response content.
        If ``as_table``, An object of class ``pd.DataFrame`` containing data from
        ``beaapi.api_request(...)`` with
        metadata stored as an attribute in ``pd.DataFrame(...).attrs``.

    Examples
    --------
    >>> import beaapi
    >>> beaspecs = {
    >>>     'UserID': beakey ,
    >>>     'Method': 'GetData',
    >>>     'datasetname': 'NIPA',
    >>>     'TableName': 'T20305',
    >>>     'Frequency': 'Q',
    >>>     'Year': 'X',
    >>> }
    >>> beaPayload = beaapi.api_request(beaspecs)
    """

    encoding_str = 'iso-8859-1'  # 'utf-8' returns decode errors

    if(not isinstance(beaspec, dict)):
        print('Please specify API parameters as a list. For example: api_request('
              '{"UserID": "YourKey", "Method": "GetData", [your remaining parameters]'
              '))')
        raise Exception('Invalid object class passed to api_request([list of API'
                        ' parameters]): ' + str(type(beaspec)) + '. Should be of'
                        ' class "dict"')

    # Change spec names to lowercase and reassign
    lower_beaspec = {k.lower(): v for k, v in beaspec.items()}
    beaspec = lower_beaspec
    # attributes(beaSpec)$names <- tolower(attributes(beaSpec)$names)

    if(not isinstance(beaspec['userid'], str)):
        raise Exception('Invalid API key of class ' + str(type(beaspec['userid'])))

    beaspec['userid'] = beaspec['userid'].replace(' ', '')
    beaspec['beaR'] = 'py_v1'

    # Some defaults for user convenience
    if not ('resultformat' in list(beaspec.keys())):
        beaspec['resultformat'] = 'json'

    if throttle and not (beaspec['resultformat'] == 'json' and (as_string or as_dict or as_table)):
        print(f"{beaspec['resultformat']} == 'json' and not {as_string} and ({as_dict} or {as_table})")
        # TODO
        import warnings
        warnings.warn("Warning: BEA API throttling is only supported for (resultformat=='json' and not as_string and (as_dict or as_table)).", UserWarning)

    if(len(beaspec['userid']) != 36):
        raise Exception('Invalid API key: ' + beaspec['userid'])
    if 'base_url' in beaspec:
        base_url = beaspec.pop('base_url')
    else:
        base_url = default_base_url
    # Parse user settings into API URL
    params = urllib.parse.urlencode(beaspec)
    bea_url = base_url + params

    if throttle:
        from .throttling_caller import throttling_data, ThrottlingCaller
        userid = beaspec['userid']
        if userid not in throttling_data:
            throttling_data[userid] = ThrottlingCaller()

        throttling_data[userid].wait_until_available()

    # Make the API call and, for now, just return the response
    try:
        with urllib.request.urlopen(bea_url) as f:
            if(f.getcode() > 200):
                raise Exception(f"Failed to retrieve data from {bea_url} with status code"
                                " {f.getcode()}")
            # beaPayload = f.read().decode(encoding_str)
            bea_payload = f
            # return(beaPayload)

            try:
                if(math.floor(bea_payload.status / 100) != 2):
                    raise Exception('Request failed. Returned HTTP status code: '
                                    + str(bea_payload['status_code']))
            except Exception:
                raise Exception('Submitted variable is not a valid https response class'
                                ' object.')

            # Give user format they want (do it in order of least modification unless
            # nothing but as_table=False specified)
            if(as_string):
                bea_content = bea_payload.read().decode(encoding_str)
                if throttle:
                    throttling_data[userid].log_query(len(bea_content))
                return(bea_content)
            else:
                if not as_dict and not as_table:
                    # TODO: can I read here and then let user read again?
                    #if throttle:
                    #    bea_content = bea_payload.read().decode(encoding_str)
                    #    throttling_data[userid].log_query(len(bea_content))
                    return(bea_payload)

                try:
                    if (as_dict):
                        from beaapi.response_to_dict import response_to_dict
                        bea_response = response_to_dict(bea_payload, is_meta=is_meta)
                        if throttle:
                            rs = bea_response["response_size"]
                            assert isinstance(rs, int)
                            throttling_data[userid].log_query(rs)
                        return(bea_response)
                    else:  # as_table
                        from beaapi.response_to_table import response_to_table
                        bea_results = response_to_table(bea_payload)
                        if throttle:
                            throttling_data[userid].log_query(bea_results.attrs["response_size"])
                        return(bea_results)
                except BEAAPIFailure as e:
                    if throttle:
                        throttling_data[userid].wait_prev_failure = True
                    raise e
                except BEAAPIResponseError as e:
                    if throttle:
                        throttling_data[userid].log_query(e.response_size, True)
                    raise e
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"BEA API: You've exceeded a rate limit (either # of requests, # of errors, or amount of data), and your requests will be blocked for the next hour. Use the throttling option to wait sufficiently next time.")
        raise e