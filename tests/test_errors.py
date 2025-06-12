import unittest
import beaapi


# For now, keep track of the API error code
# (we haven't made specific classes for them at this point)
class TestErrors(unittest.TestCase):
    def setUp(self):
        # Get key from unversioned file
        from dotenv import dotenv_values
        self.beakey = dotenv_values()["beakey"]

    def test_bad_key(self):
        # Error code 1
        self.assertRaises(beaapi.BEAAPIResponseError, beaapi.get_data_set_list,
                          'AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA')

    def test_bad_dataset(self):
        # Error Code: 20
        self.assertRaises(beaapi.BEAAPIResponseError, beaapi.get_parameter_list,
                          self.beakey, "FOOBAR")

    def test_bad_param_name(self):
        # Error Code: 31
        self.assertRaises(beaapi.BEAAPIResponseError, beaapi.get_parameter_values,
                          self.beakey, 'NIPA', 'FOOBAR')

    def test_not_implimented_dataset_paramValsFiltered(self):
        # Error Code: 34
        self.assertRaises(beaapi.BEAAPIResponseError,
                          beaapi.get_parameter_values_filtered, self.beakey, 'NIPA',
                          'Frequency', TableName='T10101', Year='X')

    def test_invalid_param_val(self):
        # Error Code: 204
        self.assertRaises(beaapi.BEAAPIResponseError, beaapi.get_data, self.beakey,
                          'UnderlyingGDPbyIndustry', Year='2013', Industry='All',
                          tableID='210', Frequency='Q')


if __name__ == '__main__':
    unittest.main()
