from typing import Optional
import pandas as pd


def update_metadata(userid: str, dataset_list: Optional[list] = None,
                    metadata_store: str = "beaapi_data", throttle: bool = True) -> int:
    """
    Updates local store of metadata. Currently only for datasets 'nipa',
    'niunderlyingdetail', and 'fixedassets'.

    Parameters
    ----------
    userid :
        Your API key.
    dataset_list :
        list of datasets to update. None will update all known datasets.
    metadata_store :
        Directory path of where to store the files. Defaults to subdirectory of current
        working directory.

    Returns
    -------
    int
        The response size from the API query.

    Examples
    --------
    >>> import beaapi
    >>> beaapi.update_metadata('yourAPIkey')
    """
    import os
    import json
    from beaapi import api_request, BEAAPIPkgException
    from .beaapi_error import no_meta_err_msg

    bea_known_meta_sets = [
        'nipa',
        'niunderlyingdetail',
        'fixedassets',
        # 'regional'
        # 'regionaldata',
        # 'regionalproduct',
        # 'regionalincome',
    ]
    if dataset_list is None:
        dataset_list = bea_known_meta_sets

    bea_meta_specs = {
        'UserID': userid ,
        'method': 'GetData',
        'datasetname': 'APIDatasetMetaData',
        'dataset': ','.join(dataset_list),
        'ResultFormat': 'json'
    }

    if not(os.path.exists(metadata_store)):
        os.makedirs(metadata_store)
        print("Created directory: " + metadata_store)

    # Get as JSON string
    bea_response_string = api_request(bea_meta_specs, as_string=True, throttle=throttle)
    assert isinstance(bea_response_string, str)

    response_size = len(bea_response_string)

    metaList = json.loads(bea_response_string)

    if(len(metaList['BEAAPI']['Datasets']) == 0):
        raise BEAAPIPkgException(no_meta_err_msg, response_size)

    metaset_info = pd.DataFrame(metaList['BEAAPI']['Datasets'], dtype='string')

    # bind dataset metadata together
    # This is a bit of a time drag, so we want to only do it if we need to
    # And do it separately for each dataset; some datasets treated differently, and
    # naming case variations make this worth doing

    proper_ds_casings = {
        "nipa": "NIPA",
        "niunderlyingdetail": "NIUnderlyingDetail",
        "fixedassets": "FixedAssets"
        # "regionalproduct": "RegionalProduct",
        # "regionalincome": "RegionalIncome"
    }

    nipa_niud_fixa_colnames = [
        'SeriesCode',
        'RowNumber',
        'LineDescription',
        'LineNumber',
        'ParentLineNumber',
        'Tier',
        'Path',
        'TableId',
        'Datasetname',
        'TableName',
        'ReleaseDate',
        'NextReleaseDate',
    ]
    ds_colnames = {
        "nipa": nipa_niud_fixa_colnames,
        "niunderlyingdetail": nipa_niud_fixa_colnames,
        "fixedassets": nipa_niud_fixa_colnames
        # "regionalproduct": "RegionalProduct",
        # "regionalincome": "RegionalIncome"
    }

    lower_datasetList = [ds.lower() for ds in dataset_list]

    # Regional data: dataset discontinued, warn user
    # if('regionaldata' in lower_datasetList):
    #     warnings.message('The RegionalData dataset has been removed from the API;'
    #                      ' please use RegionalIncome and RegionalProduct instead.')

    # iterate through listed sets
    for ds in lower_datasetList:
        # need this universally
        mask = metaset_info['Datasetname'].str.lower() == ds
        ds_mdu = metaset_info[mask]['MetaDataUpdated']
        # Handling for nipa, ni underlying detail, and fixed assets handled the same,
        # while regional product and income are handled the same
        # Here, we handle the former three.
        if ds in ['nipa', 'niunderlyingdetail', 'fixedassets']:
            api_objs = []
            for api_tab in metaList['BEAAPI']['Datasets']:
                if api_tab['Datasetname'].lower() == ds:
                    api_objs.extend(api_tab['APITable'])

            ds_tab_list = []
            ds_row_list = []
            for obj in api_objs:
                tab_part = pd.DataFrame(obj['Line'], dtype='string')
                tab_part['TableId'] = obj['TableId']
                ds_row_list.append(tab_part)

                keys_to_extract = ['TableId', 'TableName', 'ReleaseDate',
                                   'NextReleaseDate']
                obj_info = [{key: obj[key] for key in keys_to_extract}]
                ds_tab = pd.DataFrame(obj_info, dtype='string')
                ds_tab['Datasetname'] = proper_ds_casings[ds]
                ds_tab_list.append(ds_tab)

            ds_rows = pd.concat(ds_row_list)
            ds_tabs = pd.concat(ds_tab_list)

            ds_index = (ds_tabs.merge(ds_rows, on="TableId", how="right")
                        [ds_colnames[ds]])

            ds_index.assign(DatasetName=proper_ds_casings[ds])
            ds_index.assign(MetaDataUpdated=ds_mdu)
            file_name = proper_ds_casings[ds] + '.pickle'
            file_path = os.path.join(metadata_store, file_name)
            # with open(filePath, 'wb') as handle:
            #     pickle.dump(dsIndex, handle)
            pd.to_pickle(ds_index, file_path)

        # # ...And here, we handle the latter two:
        # if(ds in ['regionalproduct', 'regionalincome']):
        #   wmsg = f"No data for {proper_ds_casings[ds]}. This probably means there" + \
        #          " is a problem on our API servers; please contact " + \
        #          "Developers@bea.gov to report this issue."
        #     try:

        #         dsParams = []
        #         for datasetmeta in metaList['BEAAPI']['Datasets']:
        #             if datasetmeta['Datasetname'].lower() == ds:
        #                 dsParams.append(datasetmeta['Parameters'])
        #         if(len(dsParams) < 1):
        #             warnings.warn(wmsg)
        #         dsPages = pd.concat([pd.DataFrame(df) for df in dsParams]) \
        #                       [dsParams['ParamValue'] != 'NULL']['ParamValue']

        #         dsPageTabs = []

        #         for i in range(len(dsPages)):
        #             regDT = pd.DataFrame(dsPages[i])
        #             regDT.assign(Parameter = dsParams[i])
        #             dsPageTabs.append(regDT)

        #         dsIndex = pd.concat(dsPageTabs)

        #         dsIndex.assign(DatasetName = proper_ds_casings[ds])
        #         dsIndex.assign(MetaDataUpdated = dsMDU)
        #         fileName = proper_ds_casings[ds] + '.pickle'
        #         filePath = os.path.join(metadata_store, fileName)
        #         #with open(filePath, 'wb') as handle:
        #         #    pickle.dump(dsIndex, handle)
        #         pd.to_pickle(dsIndex, filePath)

        #     except BaseException as err:
        #         print(f"{type(err)=} error: {err=}")

    return response_size
