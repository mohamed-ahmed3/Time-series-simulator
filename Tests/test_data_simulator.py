"""
import unittest
from datetime import datetime
from unittest.mock import patch

from data_simulator import DataSimulator

"""
"""
class TestDataSimulator(unittest.TestCase):
    @patch("configuration_manager.ConfigurationManager", autospec=True)
    def setUp(self) -> None:
        self.start_date = datetime(2021, 7, 1)
        self.frequencies = ["1D", "10T", "30T", "1H", "6H", "8H"]
        self.daily_seasonality_options = ["no", "exist"]
        self.weekly_seasonality_options = ["exist", "no"]
        self.noise_levels = ["small"]  # , "large"]
        self.trend_levels = ["exist", "no"]
        self.cyclic_periods = ["exist", "no"]
        self.data_types = [""
                           "", "additive"]
        self.percentage_outliers_options = [0.05]  # , 0]
        self.data_sizes = [60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 365]

    def test_generate_success(self, configuration_mock):
        configuration_mock.assert_called()
        configuration_instance = configuration_mock.return_value
        self.simulator = DataSimulator(configuration_instance)
        result = DataSimulator.generate(self.simulator)

        self.assertIsInstance(result, tuple)


if __name__ == '__main__':
    unittest.main()
"""