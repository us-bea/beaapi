import unittest
import beaapi


class TestMain(unittest.TestCase):
    def setUp(self):
        # Get key from unversioned file
        from dotenv import dotenv_values
        self.beakey = dotenv_values()["beakey"]

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
