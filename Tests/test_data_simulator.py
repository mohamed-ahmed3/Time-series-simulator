import unittest
from datetime import datetime
import random
from unittest.mock import MagicMock
import pandas as pd

from data_simulator import DataSimulator
from configuration_manager import ConfigurationManager


class TestDataSimulator(unittest.TestCase):
    """
    Unit tests for the DataSimulator class.

    These tests verify various aspects of the DataSimulator class, including data generation,
    time series generation, and the addition of seasonality components.
    """
    def setUp(self) -> None:
        """
        Set up the test environment by defining configuration options, initializing a DataSimulator instance,
        and creating a mock ConfigurationManager.
        """
        self.start_date = datetime(2021, 7, 1)
        self.end_date = datetime(2021, 10, 2)
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

        self.freq = random.choice(self.frequencies)

        self.configuration_mock = MagicMock(spec=ConfigurationManager)
        self.data_simulator_instance = DataSimulator(self.configuration_mock)

    def test_generate(self):
        """
        Test the data generation method to ensure it yields tuples.
        """
        data_generator = self.data_simulator_instance.generate()
        for i in data_generator:
            self.assertIsInstance(i, tuple)

    def test_generate_time_series(self):
        """
        Test the generation of a time series (DatetimeIndex).
        """
        date = self.data_simulator_instance.generate_time_series(self.start_date, self.end_date, "M")
        self.assertIsInstance(date, pd.DatetimeIndex)

    def test_add_weekly_seasonality(self):
        """
        Test the addition of weekly seasonality to a time series.
        """
        date = self.data_simulator_instance.generate_time_series(self.start_date, self.end_date, self.freq)
        weekly_seasonality = self.data_simulator_instance.add_weekly_seasonality(date, self.weekly_seasonality_options,
                                                                                 self.data_types)

        self.assertIsInstance(weekly_seasonality, pd.Series)

    def test_add_daily_seasonality(self):
        """
        Test the addition of daily seasonality to a time series.
        """
        date = self.data_simulator_instance.generate_time_series(self.start_date, self.end_date, self.freq)
        weekly_seasonality = self.data_simulator_instance.add_weekly_seasonality(date, self.daily_seasonality_options,
                                                                                 self.data_types)

        self.assertIsInstance(weekly_seasonality, pd.Series)


if __name__ == '__main__':
    unittest.main()
