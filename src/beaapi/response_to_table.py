import warnings
import numpy as np
import pandas as pd
from http.client import HTTPResponse
from typing import Union

from beaapi.response_to_dict import response_to_dict
# from beaapi.get_row_data_value import get_row_data_value


def response_to_table(bea_payload: Union[list, pd.DataFrame, HTTPResponse],
                      repull: bool = False) -> pd.DataFrame:
    """
    Convert BEA API http response or list payload to pandas DataFrame,
    or transform wide DataFrame to long (or vice-versa).
    Converts LONG data frame (default API format - see response_to_dict results)
    to WIDE data (with years as columns) by default

    Parameters
    ----------
    bea_payload :
        A 'HTTPResponse' returned from beaapi.api_response(...) call to
        BEA API, an object of class 'list' returned from beaapi.response_to_dict(...),
        or an object of class 'pd.DataFrame' returned from
        beaapi.response_to_table(...).
    repull :
        Repull data from API if True, or use existing payload otherwise.

    Returns
    -------
    pd.DataFrame
        An object of class 'pd.DataFrame' containing data from beaapi.api_respons(...)
        with metadata stored as an attribute in pd.DataFrame(...).attrs.

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
    >>> bea_payload = beaapi.api_respons(beaspecs)
    """

    if(not isinstance(bea_payload, list)):
        # We want this to be reversable--we want to be able to apply this method to
        # pandas dataframe as well.
        # At the moment, we have done this in a really lazy way: Getting the data from
        # the 'params' attribute all over again in the bea2dict function.
        if(isinstance(bea_payload, pd.DataFrame) and repull):
            # Check if we have the right kind of dataframe; we should probably use
            # dataclasses to make a special class, but lazy
            if('params' in list(bea_payload.attrs.keys())):
                from beaapi import api_request
                bea_list = api_request(bea_payload.attrs['params'], as_dict=True)
            else:
                print('Must use BEA API response DataFrame, list returned from'
                      ' response_to_dict, or HTTP response from api_response() in '
                      'response_to_table function.')
                raise Exception('Submitted variable is not a valid response_to_table'
                                ' input.')
        else:
            assert isinstance(bea_payload, HTTPResponse)
            # Crash the normal way if it's not a reversion.
            # Maybe a little annoying to get the warning, but whatever.
            bea_list = response_to_dict(bea_payload)
            assert isinstance(bea_list, dict)

    # Should make our own class instead of just checking if pd.DataFrame
    if(isinstance(bea_payload, pd.DataFrame) and (not repull)):
        bea_response = bea_payload.copy()
    else:
        # response_to_dict will already check for errors
        assert isinstance(bea_list, dict)

        # Convert to pandas dataframe
        if isinstance(bea_list['Data'], list):
            bea_response = pd.DataFrame(bea_list['Data'], dtype='string')
        else:  # API weirdness (here and else): dict, when single observation
            bea_response = pd.DataFrame(bea_list['Data'], dtype='string', index=[0])
        bea_response.reset_index(drop=True, inplace=True)

        # Get metadata as attributes
        for key in bea_list.keys():
            if key not in ['Data', 'detail']:
                bea_response.attrs[key] = bea_list[key]
        # Format details specifically
        detail = bea_list['detail']
        assert isinstance(detail, dict)
        # format Dimensions
        dim_tbl = pd.DataFrame(detail['Dimensions'], dtype='string')
        dim_tbl['IsValue'] = pd.to_numeric(dim_tbl['IsValue'])
        # API weirdness: Regional dataset sometimes doesn't return Ordinal
        if 'Ordinal' in dim_tbl.columns:
            dim_tbl['Ordinal'] = pd.to_numeric(dim_tbl['Ordinal'])
        # dim_tbl = dim_tbl.set_index('Ordinal') #nice, but Ordinal not always returned
        detail['Dimensions'] = dim_tbl
        # format Notes
        if 'Notes' in detail.keys():
            if isinstance(detail['Notes'], list):
                detail['Notes'] = pd.DataFrame(detail['Notes'], dtype='string')
            else:  # dict, which happens if it's a single observation
                detail['Notes'] = pd.DataFrame(detail['Notes'], dtype='string',
                                               index=[0])
        bea_response.attrs['detail'] = detail

        # Convert things that should be numbers to numbers
        to_convert = list(dim_tbl['Name'][dim_tbl['DataType'] == "numeric"])
        for col in to_convert:
            try:
                if col == "DataValue":
                    # Automatically convert "(D)"/"(NM)" -> "" when there's a note
                    # (D)=Omitted for disclosure
                    # (NM)=Not meaningful
                    if 'NoteRef' in bea_response.columns:
                        mask1 = np.logical_and(bea_response['DataValue'] == "(D)",
                                               bea_response['NoteRef'] == "(D)")
                        mask2 = np.logical_and(bea_response['DataValue'] == "(NM)",
                                               bea_response['NoteRef'] == "(NM)")
                        bea_response.loc[np.logical_or(mask1, mask2), 'DataValue'] = ""
                    # bea_response['DataValue'] = [get_row_data_value(x)
                    #                              for x in bea_list['Data']]
                    bea_response[col] = pd.to_numeric(bea_response[col].str
                                                      .replace(",", "")
                                                      .replace("(NA)", ""))
                else:
                    bea_response[col] = pd.to_numeric(bea_response[col])
            except Exception as e:
                print("Couldn't convert column " + col + ". Error: " + str(e))

        # Do it for the ones that have line numbers
        param_vals_lower = [paramDict['ParameterValue'].lower()
                            for paramDict in bea_response.attrs['params']]
        intersect_line_num_sets = [param for param in param_vals_lower
                                   if param in ['nipa', 'niunderlyingdetail',
                                                'fixedassets']]
        if(len(intersect_line_num_sets) > 0):
            bea_response['LineNumber'] = [int(x['LineNumber'])
                                          for x in bea_list['Data']]

    if(bea_response.attrs['params'] is None):
        warnings.warn('Request response data not found; returned values may not contain'
                      ' successful BEA API response.')

    return(bea_response)
