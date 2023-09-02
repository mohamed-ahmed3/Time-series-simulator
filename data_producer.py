from abc import ABC, abstractmethod
import pandas as pd
import os


class DataProducer(ABC):
    def __init__(self, sink: str):
        self.sink = sink

    @classmethod
    def create(cls, sink: str):
        if sink.endswith(".csv"):
            return CsvDataProducer(sink)
        else:
            raise ValueError(f"Unsupported sink: {sink}")

    @abstractmethod
    def produce(self, data: dict):
        pass


class CsvDataProducer(DataProducer):
    def produce(self, data: dict):
        data_df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(self.sink), exist_ok=True)
        data_df.to_csv(self.sink, encoding='utf-8', index=False)
