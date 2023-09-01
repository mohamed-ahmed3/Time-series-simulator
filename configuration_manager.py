from abc import ABC, abstractmethod
import yaml


class ConfigurationManager(ABC):
    def __init__(self, source: str):
        self.source = source
        self.configs = self.read()

    @classmethod
    def create(cls, source: str):
        if source.endswith('.yml'):
            return YamlConfigurationManager(source)
        else:
            raise Exception(f"Unsupported source: {source}")

    @abstractmethod
    def read(self):
        pass
    
    @property
    def start_date(self):
        return self.configs['start_date']

    @property
    def frequencies(self):
        return self.configs['frequencies']
    
    @property
    def daily_seasonality_options(self):
        return self.configs['daily_seasonality_options']

    @property
    def weekly_seasonality_options(self):
        return self.configs['weekly_seasonality_options']

    @property
    def noise_levels(self):
        return self.configs['noise_levels']

    @property
    def trend_levels(self):
        return self.configs['trend_levels']

    @property
    def cyclic_periods(self):
        return self.configs['cyclic_periods']

    @property
    def data_types(self):
        return self.configs['data_types']

    @property
    def percentage_outliers_options(self):
        return self.configs['percentage_outliers_options']

    @property
    def data_sizes(self):
        return self.configs['data_sizes']


class YamlConfigurationManager(ConfigurationManager):
    def read(self):
        with open(self.source) as f:
            data = yaml.safe_load(f)

        return data

    





