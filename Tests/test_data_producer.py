import os.path
import unittest
from data_producer import DataProducer, CsvDataProducer
import pandas as pd


class TestDataProducer(unittest.TestCase):
    """
    Unit tests for the DataProducer class.

    These tests verify the functionality of the DataProducer class, including the successful
    creation of a CsvDataProducer instance based on the provided sink.
    """
    def setUp(self) -> None:
        """
        Set up the test environment by defining the 'sink' attribute.
        """
        self.sink = 'sample_datasets/meta_data.csv'

    def test_create(self):
        """
        Test the successful creation of a CsvDataProducer instance.
        """
        self.data_producer = DataProducer.create(self.sink)
        self.assertIsInstance(self.data_producer, CsvDataProducer)


class TestCsvDataProducer(unittest.TestCase):
    """
    Unit tests for the CsvDataProducer class.

    These tests verify the functionality of the CsvDataProducer class, including the successful
    production of a CSV file, checking if the file exists, and validating its content.
    """
    def setUp(self) -> None:
        """
        Set up the test environment by defining the 'sink' attribute, creating a sample data dictionary,
        and initializing a DataProducer instance.
        """
        self.sink = 'sample_datasets/meta_data.csv'
        self.my_test_dict = {"test1": ["done"],
                             "test2": [132]
                             }

        self.data_producer = DataProducer.create(self.sink)

    def test_produce(self):
        """
        Test the successful production of a CSV file and validate its content.
        """
        self.data_producer.produce(self.my_test_dict)
        self.assertTrue(os.path.exists(self.sink))

        read_data = pd.read_csv(self.sink)

        self.assertTrue(read_data.equals(pd.DataFrame(self.my_test_dict)))


if __name__ == '__main__':
    unittest.main()
