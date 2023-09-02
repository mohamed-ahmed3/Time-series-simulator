import os.path
import unittest
from data_producer import DataProducer, CsvDataProducer
import pandas as pd


class TestDataProducer(unittest.TestCase):
    def setUp(self) -> None:
        self.sink = 'sample_datasets/meta_data.csv'

    def test_create_success(self):
        self.data_producer = DataProducer.create(self.sink)
        self.assertIsInstance(self.data_producer, CsvDataProducer)


class TestCsvDataProducer(unittest.TestCase):
    def setUp(self) -> None:
        self.sink = 'sample_datasets/meta_data.csv'
        self.my_test_dict = {"test1": ["done"],
                             "test2": [132]
                             }

        self.data_producer = DataProducer.create(self.sink)

    def test_produce_success(self):
        self.data_producer.produce(self.my_test_dict)
        self.assertTrue(os.path.exists(self.sink))

        read_data = pd.read_csv(self.sink)

        self.assertTrue(read_data.equals(pd.DataFrame(self.my_test_dict)))


if __name__ == '__main__':
    unittest.main()
