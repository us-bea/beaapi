import pandas as pd


def get_parameter_values(userid: str, datasetname: str,
                         parametername: str, throttle: bool = True) -> pd.DataFrame:
    """
    Gives table of parameter values possible for a given dataset's given parametername.

    Parameters
    ----------
    userid :
        Your API key
    datasetname :
        Name of BEA dataset
    parametername :
        Name of BEA dataset's parameter

    Returns
    -------
    pd.DataFrame
        A DataFrame with the results. Typically there are two columns with possible
        values and descriptions, though the exactly names vary by dataset and
        parametername.
        When querying for 'Year' in NIPA, NIUnderlyingDetail, or FixedAssets the
        columns will be ['TableName', 'FirstAnnualYear', 'LastAnnualYear',
        'FirstQuarterlyYear', 'LastQuarterlyYear', 'FirstMonthlyYear',
        'LastMonthlyYear'].

        Attribute (``.attr``) dictionary keys:

        * **params** (*dict*) -- The user-defined query parameters.
        * **response_size** (*int*) --  The length of the API response.

    Examples
    --------
    >>> import beaapi
    >>> beaapi.get_parameter_values('yourAPIkey', 'RegionalData', 'keycode')
    """
    from beaapi import api_request

    bea_meta_specs = {
        'method': 'GetParameterValues',
        'UserID': userid,
        'datasetname': datasetname,
        'ParameterName': parametername,
        'ResultFormat': 'json'
    }

    bea_response = api_request(bea_meta_specs, as_dict=True, as_table=False,
                               is_meta=True, throttle=throttle)
    assert isinstance(bea_response, dict)
    if isinstance(bea_response['ParamValue'], list):
        tbl = pd.DataFrame(bea_response['ParamValue'], dtype='string')
    else:  # dict, which happens if it's a single observation
        tbl = pd.DataFrame(bea_response['ParamValue'], dtype='string', index=[0])
    for key in bea_response.keys():
        if key != 'ParamValue':
            tbl.attrs[key] = bea_response[key]

    return(tbl)
