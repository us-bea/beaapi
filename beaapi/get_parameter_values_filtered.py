import pandas as pd


def get_parameter_values_filtered(userid: str, datasetname: str, targetparameter: str,
                                  throttle: bool = True, **kwargs) -> pd.DataFrame:
    """
    Gives table of parameter values possible for a given dataset's given parameters.

    Parameters
    ----------
    userid :
        Your API key
    datasetname :
        Name of BEA dataset. Currently not implimented for 'NIPA',
        'NIUnderlyingDetail','MNE', 'FixedAssets', and 'APIDatasetMetaData'.
    targetparameter :
        Name of BEA dataset's parameter
    **kwargs :
        Other parameter-value pairs.

    Returns
    -------
    pd.DataFrame
        A DataFrame with variables 'Key' and 'Desc' showing the possible options.

        Attribute (``.attr``) dictionary keys:

        * **params** (*dict*) -- The user-defined query parameters.
        * **response_size** (*int*) --  The length of the API response.

    Examples
    --------
    >>> import beaapi
    >>> beaapi.get_parameter_values_filtered(beakey, 'Regional', 'Year',
    >>>                                      TableName='CAINC5N', GeoFips='01001')
    """
    from beaapi import api_request

    spec = kwargs.copy()
    spec['method'] = 'GetParameterValuesFiltered'
    spec['ResultFormat'] = 'json'
    spec['UserID'] = userid
    spec['TargetParameter'] = targetparameter
    spec['datasetname'] = datasetname

    bea_response = api_request(spec, as_dict=True, as_table=False, is_meta=True,
                               throttle=throttle)
    assert isinstance(bea_response, dict)
    if isinstance(bea_response['ParamValue'], list):
        tbl = pd.DataFrame(bea_response['ParamValue'], dtype='string')
    else:  # dict, which happens if it's a single observation
        tbl = pd.DataFrame(bea_response['ParamValue'], dtype='string', index=[0])
    for key in bea_response.keys():
        if key != 'ParamValue':
            tbl.attrs[key] = bea_response[key]

    return(tbl)
