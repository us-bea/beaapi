from typing import Dict


def get_row_data_value(row: Dict[str, str]) -> float:
    """
    Returns numeric DataValue from a single row (dict) of API response 'Data' list.

    Parameters
    ----------
    row :
        Single API observation.

    Returns
    -------
    float
        The value of the observation is returned by the BEA API as a string; this
        converts it to a float.
        This probably didn't need to be its own function; there are other steps in this
        project that would have made more sense to do this with.
    Examples
    --------
    >>> import beaapi.get_row_data_value
    >>> beaapi.get_row_data_value.get_row_data_value({'DataValue': "1,337"})
    """

    str_val = row['DataValue'].replace(',', '')
    if str_val == '':
        return float("nan")
    return float(str_val)
