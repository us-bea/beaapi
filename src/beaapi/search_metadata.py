import pandas as pd


def search_metadata(search_term: str, userid: str = None,
                    metadata_store: str = "beaapi_data",
                    fuzzy: bool = False, throttle: bool = True) -> pd.DataFrame:
    """
    Searches metadata for datasets. Currently works with datasets 'nipa',
    'niunderlyingdetail', and 'fixedassets'.

    If userid is provided, an API request is made to see to see if new metadata
    is available, and if so ``update_metadata()`` will be called.

    Searching without the userid is not advised.
    If you would like to retain metadata for posterity, please copy it from the
    "beaapi_data" area of your directory to elsewhere on your machine;
    this will help prevent accidental overwrite, and will not interfere with the
    "freshness" of your searches.


    Parameters
    ----------
    search_term :
        String to search for
    userid :
        Your API key. Optional if metadata already stored locally.
    metadata_store :
        Directory path of where to store the files. Defaults to subdirectory of current
        working directory.
    fuzzy :
        Try to use fuzzy string matching via the ``fuzzywuzzy`` module (must be
        installed).

    Returns
    -------
    pd.DataFrame
        A DataFrame with relevant results.

        Attribute (``.attr``) dictionary keys:

        * **response_size** (*int*) --  The length of the API response (0 if none).

    Examples
    --------
    >>> import beaapi
    >>> beaapi.search_metadata('Gross Domestic', 'yourAPIkey')
    """
    import warnings
    import os
    import numpy as np
    from beaapi import update_metadata, api_request

    if userid is None:
        warnings.warn('Searching without specifying userid, e.g., search_metadata('
                      '"tobacco", userid = "[your 36-character API key]") is not '
                      'recommended, as the key is needed to update locally stored '
                      'metadata.')

    response_size = 0
    # Instead of using a consistent dir, I suggest we just use the working dir
    if not(os.path.exists(metadata_store)):
        os.makedirs(metadata_store)
        print("Created directory: " + metadata_store)

    bea_meta_files = [f for f in os.listdir(metadata_store)
                      if ((os.path.isfile(os.path.join(metadata_store, f)))
                          and (os.path.splitext(f)[1] == '.pickle'))]

    bea_meta_files_times = [{'Dataset': os.path.splitext(f)[0],
                             'mtime': pd.to_datetime(os.path.getmtime(
                                 os.path.join(metadata_store, f)), unit='s')}
                            for f in bea_meta_files]

    bea_meta_mtime = pd.DataFrame(bea_meta_files_times)
    # Add FixedAssets in future, but regionaldata was previously merged into
    # regionalproduct and regionalincome on the API, and now those datasets have been
    # merged into "Regional"
    bea_known_meta_sets = [
        'nipa',
        'niunderlyingdetail',
        'fixedassets',
        # 'regional' #TODO: Add regional in
        # 'regionaldata',
        # 'regionalproduct',
        # 'regionalincome',
    ]

    # Check to see if this is the first time using the search function (or missing
    # files); if so, update all metadata currently handled.
    if (len(bea_meta_files) < len(bea_known_meta_sets)):
        # Create directory and make single call to get all metadata if there are
        # missing meta .RData files
        print('Creating first-time local copy of metadata for all datasets - only done'
              ' once in working directory.')
        print('Datasets will be updated only if timestamps indicate metadata obsolete'
              ' in future searches, and only obsolete metadata sets will be updated.')

        if userid is None:
            raise Exception("No API key provided")
        response_size = update_metadata(userid, bea_known_meta_sets, metadata_store,
                                        throttle=throttle)

    else:
        if userid is not None:
            # Make a "GetParameterValues" call to get timestamps of latest metadata
            # update
            bea_meta_time_spec = {
                'UserID': userid ,
                'method': 'GetParameterValues',
                'datasetname': 'APIDatasetMetaData',
                'parametername': 'dataset',
                'ResultFormat': 'json'
            }

            # Get metadata response with timestamps we need to check for updates as list
            bea_meta_params = api_request(bea_meta_time_spec, as_dict=True,
                                          as_table=False, is_meta=True,
                                          throttle=throttle)
            assert isinstance(bea_meta_params, dict)
            response_size = int(bea_meta_params['response_size'])
            bea_meta_info = pd.DataFrame(bea_meta_params['ParamValue'])

            try:
                # If JSON has been updated, set check param = false
                time_comp = (bea_meta_mtime.merge(bea_meta_info, on="Dataset",
                                                  how="right")
                             [['Dataset', 'mtime', 'JSONUpdateDate']])

                time_comp['APImtime'] = pd.to_datetime(time_comp['JSONUpdateDate'],
                                                       format="%Y-%m-%dT%H:%M:%S")

                both_valid = np.logical_and(~pd.isnull(time_comp['APImtime']),
                                            ~pd.isnull(time_comp['mtime']))
                l_earlier = time_comp['APImtime'] > time_comp['mtime']
                local_outdated_mask = np.logical_and(both_valid, l_earlier)
                local_miss_mask = np.logical_and(pd.isnull(time_comp['mtime']),
                                                 ~pd.isnull(time_comp['APImtime']))
                l_outdate_or_miss = np.logical_or(local_outdated_mask, local_miss_mask)
                outdated_local_meta = time_comp['Dataset'][l_outdate_or_miss]
                bea_meta_first_to_cache = local_miss_mask.sum() > 0

            except Exception:
                warnings.warn("API metadata mofication time table structure changed.\n"
                              " Check for package update")
                bea_meta_first_to_cache = True
                response_size += update_metadata(userid, bea_known_meta_sets,
                                                 throttle=throttle)

            lowerlocalmeta = [localmeta.lower() for localmeta in outdated_local_meta]
            newy_known = list(set(lowerlocalmeta) - set(bea_known_meta_sets))
            if (len(newy_known) > 0):
                warnings.warn('BEA API contains newly-available metadata for datasets'
                              'not handled. \nThis version of beaapi is either not the'
                              ' latest, or will soon be replaced.')
                outdated_local_meta = [localmeta for localmeta in outdated_local_meta
                                       if localmeta.lower() in bea_known_meta_sets]

            if(bea_meta_first_to_cache):
                print("Updating metadata as first to cache metadata for some datasets.")
                response_size += update_metadata(userid, bea_known_meta_sets,
                                                 throttle=throttle)
            else:
                if(len(outdated_local_meta) > 0):
                    print("Updating metadata as there are outdated local files.")
                    lowerlocalmeta = [localmeta.lower()
                                      for localmeta in outdated_local_meta]
                    response_size += update_metadata(userid, lowerlocalmeta,
                                                     throttle=throttle)

    bea_meta_files = [os.path.join(metadata_store, file)
                      for file in os.listdir(path=metadata_store)]

    bea_metadata = pd.concat([pd.read_pickle(file) for file in bea_meta_files])

    if fuzzy:
        from fuzzywuzzy import fuzz
        # from fuzzywuzzy import process
        row_match_scores = []
        for row in bea_metadata.index:
            score = 0

            for col in bea_metadata.columns:
                score += fuzz.ratio(search_term,
                                    bea_metadata.iloc[row][col]) / 100

            row_match_scores.append(score)

        searched_df = bea_metadata.copy()
        searched_df["SearchScore"] = row_match_scores

        searched_df.sort_values(by='SearchScore', ascending=False, inplace=True,
                                ignore_index=True)
    else:
        mask = bea_metadata.apply(lambda x: x.str.contains(search_term)).any(axis=1)
        searched_df = bea_metadata[mask]

    searched_df.attrs['response_size'] = response_size
    return searched_df
