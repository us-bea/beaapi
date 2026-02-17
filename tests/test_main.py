import unittest
import beaapi
import pandas as pd


class TestMain(unittest.TestCase):
    def setUp(self):
        # Get key from unversioned file
        from dotenv import dotenv_values
        self.beakey = dotenv_values()["beakey"]

    def test_new_dataset(self):
        from unittest.mock import patch
        fake_response = """{"BEAAPI":{"Request":{"RequestParam":[{"ParameterName":"USERID","ParameterValue":"redacted"},{"ParameterName":"METHOD","ParameterValue":"GETDATA"},{"ParameterName":"DATASETNAME","ParameterValue":"REGIONAL"},{"ParameterName":"TABLENAME","ParameterValue":"CAGDP2"},{"ParameterName":"LINECODE","ParameterValue":"64"},{"ParameterName":"YEAR","ParameterValue":"2018"},{"ParameterName":"GEOFIPS","ParameterValue":"01001"},{"ParameterName":"RESULTFORMAT","ParameterValue":"JSON"}]},"Results":{"Statistic":"Gross Domestic Product (GDP): Management of companies and enterprises","UnitOfMeasure":"Thousands of dollars","PublicTable":"CAGDP2 Gross domestic product (GDP) by county and metropolitan area","UTCProductionTime":"2025-07-25T14:25:45.980","NoteRef":" ","Dimensions":[{"Name":"Code","DataType":"string","IsValue":"0"},{"Name":"GeoFips","DataType":"string","IsValue":"0"},{"Name":"GeoName","DataType":"string","IsValue":"0"},{"Name":"TimePeriod","DataType":"string","IsValue":"0"},{"Name":"DataValue","DataType":"numeric","IsValue":"1"},{"Name":"CL_UNIT","DataType":"string","IsValue":"0"},{"Name":"UNIT_MULT","DataType":"numeric","IsValue":"0"}],"Data":[{"Code":"CAGDP2-64","GeoFips":"01001","GeoName":"Autauga","TimePeriod":"2018","CL_UNIT":"Thousands of dollars","UNIT_MULT":"3","DataValue":"0","NoteRef":"(D)"}],"Notes":[{"NoteRef":" ","NoteText":"notes"}]}}}"""
        with patch('http.client.HTTPResponse.read', return_value=fake_response.encode('iso-8859-1')):
            beaapi.get_data(self.beakey, datasetname='new_DATASETNAME', TableName='Table1', Frequency='A', Year='2015')

    def test_throttle_bug(self):
        beaapi.throttling_caller.throttling_data[self.beakey] = beaapi.throttling_caller.ThrottlingCaller()
        old_wait = beaapi.throttling_caller.throttling_data[self.beakey].max_secs_wait
        beaapi.throttling_caller.throttling_data[self.beakey].max_secs_wait = 2 #for testing don't wait full 60 secs
        
        # test that it waits after previous failure
        beaapi.throttling_caller.throttling_data[self.beakey].wait_prev_failure = True
        beaapi.get_data_set_list(self.beakey)

        from unittest.mock import patch
        fake_time = pd.Timestamp('2025-05-05 05:05:05.000000')
        with patch('pandas.Timestamp.now', return_value=fake_time):
            # test MAX_REQUESTS_PER_MINUTE
            beaapi.throttling_caller.throttling_data[self.beakey].rel_queries = pd.DataFrame({
                'time': [fake_time] * beaapi.MAX_REQUESTS_PER_MINUTE,
                'size': [0] * beaapi.MAX_REQUESTS_PER_MINUTE,
                'errors': [0] * beaapi.MAX_REQUESTS_PER_MINUTE
            })
            beaapi.get_data_set_list(self.beakey)

            # test MAX_DATA_PER_MINUTE
            beaapi.throttling_caller.throttling_data[self.beakey].rel_queries = pd.DataFrame({
                'time': [fake_time],
                'size': [beaapi.MAX_DATA_PER_MINUTE],
                'errors': [0]
            })
            beaapi.get_data_set_list(self.beakey)

            beaapi.throttling_caller.throttling_data[self.beakey].rel_queries = pd.DataFrame({
                'time': [fake_time]*2,
                'size': [beaapi.MAX_DATA_PER_MINUTE/2]*2,
                'errors': [0]*2
            })
            beaapi.get_data_set_list(self.beakey)

            # test MAX_ERRORS_PER_MINUTE
            beaapi.throttling_caller.throttling_data[self.beakey].rel_queries = pd.DataFrame({
                'time': [fake_time] * beaapi.MAX_ERRORS_PER_MINUTE,
                'size': [0] * beaapi.MAX_ERRORS_PER_MINUTE,
                'errors': [1] * beaapi.MAX_ERRORS_PER_MINUTE
            })
            beaapi.get_data_set_list(self.beakey)

        beaapi.throttling_caller.throttling_data[self.beakey].max_secs_wait = old_wait

    def test_attrs_in_df_bug(self):
        bea_tbl = beaapi.get_data(self.beakey, datasetname='NIPA', TableName='T20305', Frequency='Q', Year='2015')
        t2 = beaapi.to_wide_vars_in_cols(bea_tbl)
        repr(t2)


    def test_readme_fns(self):
        # A quick test of the main functions
        import tempfile
        import numpy as np

        df = beaapi.get_data_set_list(self.beakey)
        # TODO: Do any other key ones.
        #print(df)
        #print(df.dtypes)
        df = beaapi.get_parameter_list(self.beakey, 'NIPA')
        #print(df)
        #print(df.dtypes)
        df = beaapi.get_parameter_values(self.beakey, 'NIPA', 'Frequency')
        #print(df)
        #print(df.dtypes)
        df = beaapi.get_parameter_values_filtered(self.beakey, 'ITA',
                                             targetparameter='Indicator',
                                             AreaOrCountry="China",
                                             Frequency="A", Year="2011")
        #print(df)
        #print(df.dtypes)

        with tempfile.TemporaryDirectory() as test_data_dir:
            beaapi.update_metadata(self.beakey, metadata_store=test_data_dir)
            beaapi.search_metadata('Gross domestic', metadata_store=test_data_dir, userid=self.beakey)
            beaapi.search_metadata('Gross domestic', metadata_store=test_data_dir, userid=self.beakey)

        df = beaapi.get_data(self.beakey, datasetname='NIPA', TableName='T20305',
                        Frequency='Q', Year='2024')
        ##print(df)
        # print(df.dtypes)
        self.assertTrue(df.dtypes['LineNumber']=='int64' and df.dtypes['UNIT_MULT']=='int64' and df.dtypes['DataValue']=='int64')
        df = beaapi.get_data(self.beakey, datasetname='NIPA', TableName='T10101',
                        Frequency='A', Year='2024')
        # print(df)
        # print(df.dtypes)
        self.assertTrue(df.dtypes['LineNumber']=='int64' and df.dtypes['UNIT_MULT']=='int64' and df.dtypes['DataValue']=='float64')

        self.assertTrue(True)  # So it's marked as a test. Probably there's better way

    def test_num_datasets(self):
        # Test the number of datasets returned by get_data_set_list
        datasets = beaapi.get_data_set_list(self.beakey)
        self.assertEqual(len(datasets), 13, "Expected 13 datasets but got a different number")


if __name__ == '__main__':
    unittest.main()
