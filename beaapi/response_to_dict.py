import json
# import xml.etree.ElementTree as ET #So far not needed
import urllib.request
import urllib.parse
from http.client import HTTPResponse
from typing import Dict, Union
from beaapi import BEAAPIResponseError, BEAAPIFailure
from .beaapi_error import (html_error_msg, empty_err_msg, no_data_node_err_msg,
                           multiple_err_msg)


def response_to_dict(bea_payload: HTTPResponse,
                     is_meta: bool = False) -> Dict[str, Union[str, int]]:
    """
    Convert BEA API http response payload to list.

    Parameters
    ----------
    bea_payload :
        An 'HTTPResponse' returned from beaapi.api_response(...) call to
        BEA API.
    isMeta :
        Is this a metadata request from beaapi.get_data_set_list,
        beaapi.get_parameter_list, or beaapi.get_parameter_values?
        If True, data will be returned with only partial transformation (default: False)

    Returns
    -------
    dict
        The name is a little misleading here, as it is a holdover from the R version of
        this package.
        Is a dict x with x['Data'], x['detail'], and x['params'] keys if query succeeds.
        If query fails, this warns the user and returns the json.loads() dict of full
        API response.

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
    >>>     'ResultFormat': 'json'
    >>> }
    >>> bea_payload = beaapi.api_response(beaspecs, as_table=False)
    >>> beaList = beaapi.response_to_dict(bea_payload)
    """

    # In the R version, I gave up on parsing it identically and just re-pull data as
    # JSON; I may be able to avoid doing that here.
    encoding_str = 'iso-8859-1'  # 'utf-8' returns decode errors
    # Mypy for some reason doesn't think HTTPResponse has an url attr !? Ignoring
    if(bea_payload.url.find("resultformat=xml") > -1):  # type: ignore
        bea_url = bea_payload.url.replace("resultformat=xml",  # type: ignore
                                          "resultformat=json")
        try:
            # We don't throttle here, but from the calling function api_requests (also via response_to_table)
            with urllib.request.urlopen(bea_url) as f:
                bin_content = f.read()
                response_size = len(bin_content)
                bea_content = bin_content.decode(encoding_str)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"BEA API: You've exceeded a rate limit (either # of requests, # of errors, or amount of data), and your requests will be blocked for the next hour. Use the throttling option to wait sufficiently next time.")
            raise e

    else:
        bin_content = bea_payload.read()
        response_size = len(bin_content)
        bea_content = bin_content.decode(encoding_str)

    if bea_content == '':
        raise BEAAPIFailure(empty_err_msg)

    try:
        bea_response = json.loads(bea_content)
    except json.JSONDecodeError as e:
        if "<html>" in e.doc[:8] or "</html>" in e.doc[-9:]:
            # We got an HTML error back.
            # For the second type, the front looks like json, but then starting on a
            # new line is the html error. Probably shouldn't trust the json response
            raise BEAAPIFailure(html_error_msg)
        print("Unknown response format. Maybe a query error. "
              "Check e.doc on the decode error.")
        raise e

    def gen_error(error_node, response_size):
        # Error can be in beaResponse['BEAAPI'] or beaResponse['BEAAPI']['Results']
        # The field 'number' is just for numbering errors (as there may be several)

        if isinstance(error_node, list):  # sometimes multiple errors listed
            err = BEAAPIResponseError(multiple_err_msg, response_size)
            setattr(err, 'messages', [e['error'] for e in error_node])
            return(err)

        error_code = ''
        if 'APIErrorCode' in error_node:
            error_code = error_node['APIErrorCode']

        error_desc = ""
        if 'APIErrorDescription' in error_node:
            error_desc = error_node['APIErrorDescription']
        if 'error' in error_node:
            error_desc = error_node['error']

        # Sometimes there's other keys like AdditionalDetails
        error_details = [k + ": " + str(error_node[k]) for k in error_node.keys()
                         if k not in ["APIErrorCode", 'number', 'APIErrorDescription',
                                      'error']]
        error_details_str = " " + ". ".join(error_details)

        err = BEAAPIResponseError(error_desc + error_details_str, response_size)
        if error_code != "":
            setattr(err, 'APIErrorCode', error_code)

        return(err)

    if('error' in (map(lambda x: x.lower(), bea_response['BEAAPI'].keys()))):
        err = gen_error(bea_response['BEAAPI']['Error'], response_size)
        raise err

    # API weirdness: these are 1-unit lists for GetData for datasets GDPbyIndustry, IIP,
    # InputOutput, and underlyingGDPbyIndustry
    if ('Results' in bea_response['BEAAPI']
       and isinstance(bea_response['BEAAPI']['Results'], list)
       and len(bea_response['BEAAPI']['Results']) == 1):
        bea_response['BEAAPI']['Results'] = bea_response['BEAAPI']['Results'][0]

    if('error' in (map(lambda x: x.lower(), bea_response['BEAAPI']['Results'].keys()))):
        err = gen_error(bea_response['BEAAPI']['Results']['Error'], response_size)
        raise err

    if is_meta:
        bea_list = bea_response['BEAAPI']['Results']
        bea_list['params'] = bea_response['BEAAPI']['Request']['RequestParam']
    else:
        bea_list = {}
        if 'Data' in bea_response['BEAAPI']:  # API weirdness: IIP
            bea_list['Data'] = bea_response['BEAAPI']['Data']
            bea_list['detail'] = bea_response['BEAAPI']['Results']
        else:
            if 'Data' not in bea_response['BEAAPI']['Results']:
                raise BEAAPIResponseError(no_data_node_err_msg, response_size)
            bea_list['Data'] = bea_response['BEAAPI']['Results'].pop('Data')
            bea_list['detail'] = bea_response['BEAAPI']['Results']

        bea_list['params'] = bea_response['BEAAPI']['Request']['RequestParam']
    bea_list['response_size'] = response_size

    return(bea_list)
