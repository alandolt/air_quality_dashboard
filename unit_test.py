import unittest
from air_quality_dashboard.data_parser.local_data import LocalData
import pandas as pd


class TestLocalData(unittest.TestCase):

    def test_load_local_air_quality_data(self):
        localdata1 = LocalData()
        self.assertIsNotNone(localdata1.df)

    def test_update_local_air_quality_data(self):
        localdata1 = LocalData()
        self.assertIsNotNone(localdata1.df)

    def test_min_date(self):
        localdata1 = LocalData()
        localdata1.df = pd.read_pickle(
            "data_for_unit_testing/local_air_quality_data_Switzerland.xz",
            compression="xz",
        )
        self.assertEqual(
            localdata1.min_date(),
            "2024-01-05 21:00",
            "Lowest data string should be 2024-01-05 21:00",
        )

    def test_init(self):
        # with this condition, we see if the programs exit, if no valid data source is supplied
        self.assertRaises(
            SystemExit,
            LocalData,
            "no_valid_url_supplied",
            "no_valid_local_data_pickle file",
        )
        # with this condition, we see if the programs exit, if no valid data source is supplied. Contrary to above,
        # we should get a Timeout error (but stillw with a SystemExit)
        self.assertRaises(
            SystemExit,
            LocalData,
            "http://www.no_valid_url_supplied.com",
            "no_valid_local_data_pickle file",
        )
        # valid data source is supplied, but no valid url for updating. The program should exit
        self.assertRaises(SystemExit, LocalData, "no_valid_url_supplied", "Switzerland")


if __name__ == "__main__":
    unittest.main()
