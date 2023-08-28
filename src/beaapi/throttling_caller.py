# Provides a way to self-throttle api calls. Used by API calls.
# Make sure places that raise BEAAPIFailure/BEAAPIResponseError are wrapped
# to update throttling data if required (currently all in api_request)
#
# If the user exceeds this a `urllib.error.HTTPError` is raised (with the error's
# `.code==429`) and they will be denied access for 1 hour.
#
# Like https://github.com/tomasbasham/ratelimit but incorporates size limits
import time
from typing import Callable, Union, Optional, Dict
import pandas as pd
import beaapi


class ThrottlingCaller(object):
    # An instance of this class encapsulates information to self-throttle api calls.
    # Just wrap a bea callable and they will be called slow
    # enough to not go over the BEA limits.
    def __init__(self):
        self.rel_queries = pd.DataFrame({'time': pd.Series(dtype='datetime64[ns]'),
                                         'size': pd.Series(dtype='float'),
                                         'errors': pd.Series(dtype='int')})
        self.wait_prev_failure = False

    def wait_until_available(self) -> None:
        # If the previous one failed, it might have been a large volume,
        # but we won't know. So be conservative
        if self.wait_prev_failure:
            time.sleep(60)
            self.wait_prev_failure = False
            return

        # wait till not-too-many requests
        n = pd.Timestamp.now()
        mask = self.rel_queries['time'] >= n - pd.Timedelta(1, "minute")
        if self.rel_queries[mask].shape[0] >= beaapi.MAX_REQUESTS_PER_MINUTE:
            # allowable in the last minute
            n_not_allow = self.rel_queries.shape[0] - beaapi.MAX_REQUESTS_PER_MINUTE + 1
            allowable_mask = self.rel_queries.index >= n_not_allow
            oldest_allowable_ts = self.rel_queries[allowable_mask]['time'].min()
            time.sleep(60 - (n - oldest_allowable_ts).seconds + 1)

        # wait till not too much volume
        n = pd.Timestamp.now()
        mask = self.rel_queries['time'] >= n - pd.Timedelta(1, "minute")
        if self.rel_queries['size'][mask].sum() >= beaapi.MAX_DATA_PER_MINUTE:
            rev_cumsum = self.rel_queries.iloc[::-1]['size'].cumsum().iloc[::-1]
            allowable_mask = rev_cumsum < beaapi.MAX_DATA_PER_MINUTE
            oldest_allowable_ts = self.rel_queries[allowable_mask]['time'].min()
            time.sleep(60 - (n - oldest_allowable_ts).seconds + 1)

        # wait till not-too-many errors
        n = pd.Timestamp.now()
        mask = self.rel_queries['time'] >= n - pd.Timedelta(1, "minute")
        if self.rel_queries['errors'][mask].sum() >= beaapi.MAX_ERRORS_PER_MINUTE:
            rev_cumsum = self.rel_queries.iloc[::-1]['errors'].cumsum().iloc[::-1]
            allowable_mask = rev_cumsum < beaapi.MAX_ERRORS_PER_MINUTE
            oldest_allowable_ts = self.rel_queries[allowable_mask]['time'].min()
            time.sleep(60 - (n - oldest_allowable_ts).seconds + 1)

    def wait_full_reset(self) -> None:
        time.sleep(60)

    def single_call(self, beacall: Callable) -> None:
        self.wait_until_available()
        try:
            bea_tbl = beacall()
        except beaapi.BEAAPIFailure as e:
            self.wait_prev_failure = True
            raise e
        except beaapi.BEAAPIResponseError as e:
            self.log_query(e.response_size, True)
            raise e
        self.log_query(bea_tbl.attrs["response_size"])
        return(bea_tbl)

    def log_query(self, size: Union[int, float], err: bool = False,
                  n: Optional[pd.Timestamp] = None) -> None:
        if n is None:
            n = pd.Timestamp.now()

        # Otherwise get "PerformanceWarning: DataFrame is highly fragmented."
        # from normal insertion rel_queries.loc[self.rel_queries.shape[0]] = (n, size)
        self.rel_queries = pd.concat([self.rel_queries,
                                      pd.DataFrame({'time': [n], 'size': [size],
                                                    'errors':[int(err)]})],
                                     axis=0).reset_index(drop=True)


# Global to keep track of throlling data (by )
throttling_data : Dict[str, ThrottlingCaller] = {}
