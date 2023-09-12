from abc import ABC, abstractmethod
import pandas as pd
import os


class DataProducerFileCreation:

    @classmethod
    def create(cls, sink: str):
        """
        Factory method to create a specific DataProducer instance based on the sink type.

        Parameters:
            sink (str): The destination where data will be produced.

        Returns:
            DataProducer: An instance of a DataProducer subclass (e.g., CsvDataProducer).

        Raises:
            ValueError: If the sink type is not supported.
        """
        if sink.endswith(".csv"):
            return CsvDataProducer(sink)
        else:
            raise ValueError(f"Unsupported sink: {sink}")


class DataProducer(ABC):
    """
    An abstract base class for data producers.

    Attributes:
        sink (str): The destination where data will be produced.
    """

    def __init__(self, sink: str):
        """
        Initialize a DataProducer instance.

        Parameters:
            sink (str): The destination where data will be produced.
        """
        self.sink = sink

    @abstractmethod
    def produce(self, data: dict):
        pass


class CsvDataProducer(DataProducer):
    def produce(self, data: dict):
        """
        Produce data to the specified destination by saving it as a CSV file.

        This method takes a dictionary of data and saves it as a CSV file to the destination
        specified during the object's initialization.

        Parameters:
            data (dict): A dictionary containing the data to be saved to the CSV file.

        """
        data_df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(self.sink), exist_ok=True)
        data_df.to_csv(self.sink, encoding='utf-8', index=False)