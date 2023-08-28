import pandas as pd


def get_data_set_list(userid: str, throttle: bool = True) -> pd.DataFrame:
    """
    Returns a table of all datasets.

    Parameters
    ----------
    userid :
        Your API key

    Returns
    -------
    pd.DataFrame
        A DataFrame with variables 'DatasetName' and 'DatasetDescription'.

        Attribute (``.attr``) dictionary keys:

        * **params** (*dict*) -- The user-defined query parameters.
        * **response_size** (*int*) --  The length of the API response.
    Examples
    --------
    >>> import beaapi
    >>> beaapi.get_data_set_list('yourAPIkey')
    """
    from beaapi import api_request

    # Set up spec for it
    bea_meta_specs = {
        'method': 'GetDataSetList',
        'UserID': userid,
        'ResultFormat': 'json'
    }

    # Set list using api_response
    bea_response = api_request(bea_meta_specs, as_dict=True, as_table=False,
                               is_meta=True, throttle=throttle)
    assert isinstance(bea_response, dict)
    tbl = pd.DataFrame(bea_response['Dataset'], dtype='string')
    for key in bea_response.keys():
        if key != 'Dataset':
            tbl.attrs[key] = bea_response[key]

    return(tbl)
