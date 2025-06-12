import pandas as pd


def get_parameter_list(userid: str, datasetname: str,
                       throttle: bool = True) -> pd.DataFrame:
    """
    Gives list of parameters possible for a given dataset.

    Parameters
    ----------
    userid :
        Your API key
    datasetname :
        Name of BEA dataset

    Returns
    -------
    pd.DataFrame
        A DataFrame with the variables: 'ParameterName', 'ParameterDataType',
        'ParameterDescription', 'ParameterIsRequiredFlag', 'ParameterDefaultValue',
        'MultipleAcceptedFlag', 'AllValue'.

        Attribute (``.attr``) dictionary keys:

        * **params** (*dict*) -- The user-defined query parameters.
        * **response_size** (*int*) --  The length of the API response.

    Examples
    --------
    >>> import beaapi
    >>> beaapi.get_parameter_list('yourAPIkey', 'RegionalData')
    """

    from beaapi import api_request

    bea_meta_specs = {
        'UserID': userid ,
        'method': 'GetParameterList',
        'datasetname': datasetname,
        'ResultFormat': 'json'
    }

    bea_response = api_request(bea_meta_specs, as_dict=True, as_table=False,
                               is_meta=True, throttle=throttle)
    assert isinstance(bea_response, dict)
    if isinstance(bea_response['Parameter'], list):
        tbl = pd.DataFrame(bea_response['Parameter'], dtype='string')
    else:  # API weirdness (here and else): dict, when single observation
        tbl = pd.DataFrame(bea_response['Parameter'], dtype='string', index=[0])
    tbl['MultipleAcceptedFlag'] = pd.to_numeric(tbl['MultipleAcceptedFlag'])
    tbl['ParameterIsRequiredFlag'] = pd.to_numeric(tbl['ParameterIsRequiredFlag'])

    for key in bea_response.keys():
        if key != 'Parameter':
            tbl.attrs[key] = bea_response[key]

    return(tbl)
