import unittest
import beaapi


class TestMain(unittest.TestCase):
    def setUp(self):
        # Get key from unversioned file
        import os
        from dotenv import load_dotenv
        load_dotenv()
        self.beakey = os.environ.get("beakey")

    def test_readme_fns(self):
        # A quick test of the main functions
        import tempfile

        beaapi.get_data_set_list(self.beakey)
        beaapi.get_parameter_list(self.beakey, 'NIPA')
        beaapi.get_parameter_values(self.beakey, 'NIPA', 'Frequency')
        beaapi.get_parameter_values_filtered(self.beakey, 'ITA',
                                             targetparameter='Indicator',
                                             AreaOrCountry="China",
                                             Frequency="A", Year="2011")

        with tempfile.TemporaryDirectory() as test_data_dir:
            beaapi.update_metadata(self.beakey, metadata_store=test_data_dir)
            beaapi.search_metadata('Gross domestic', metadata_store=test_data_dir, userid=self.beakey)

        beaapi.get_data(self.beakey, datasetname='NIPA', TableName='T20305',
                        Frequency='Q', Year='X')

        self.assertTrue(True)  # So it's marked as a test. Probably there's better way


if __name__ == '__main__':
    unittest.main()
