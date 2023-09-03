from abc import ABC, abstractmethod
from typing import List

import yaml
import json
from datetime import datetime


class ConfigurationManager(ABC):
    """
    Abstract class to make the configuration manager extensible
    methods:
        --init--
        create: created the instance
        read: abstract method
        property methods to get the data
    """

    def __init__(self, source: str):
        """
        Initialize the object with the source

        Parameters:
            source: The source of the data. Can be yaml file or json file
        """
        self.source = source
        self.configs = self.read()

    @classmethod
    def create(cls, source: str):
        """
        Creates an instance from the chosen source.

        Parameters:
            source: The source of the data. Can be yaml file or json file
        
        """
        if source.endswith('.yml'):
            return YamlConfigurationManager(source)

        elif source.endswith('.json'):
            return JsonConfigurationManager(source)

        else:
            raise Exception(f"Unsupported source: {source}")

    @abstractmethod
    def read(self):
        pass

    @property
    def start_date(self):
        """
        Gets the start_date from the file

        return:
            start_date
        """
        return self.configs['start_date']

    @property
    def frequencies(self):
        """
        Gets the frequencies from the file

        return:
            frequencies
        """
        return self.configs['frequencies']

    @property
    def daily_seasonality_options(self):
        """
        Gets the daily_seasonality_options from the file

        return:
            daily_seasonality_options
        """
        return self.configs['daily_seasonality_options']

    @property
    def weekly_seasonality_options(self):
        """
        Gets the weekly_seasonality_options from the file

        return:
            weekly_seasonality_options
        """
        return self.configs['weekly_seasonality_options']

    @property
    def noise_levels(self):
        """
        Gets the noise_levels from the file

        return:
            noise_levels
        """
        return self.configs['noise_levels']

    @property
    def trend_levels(self):
        """
        Gets the trend_levels from the file

        return:
            trend_levels
        """
        return self.configs['trend_levels']

    @property
    def cyclic_periods(self):
        """
        Gets the cyclic_periods from the file

        return:
            cyclic_periods
        """
        return self.configs['cyclic_periods']

    @property
    def data_types(self):
        """
        Gets the data_types from the file

        return:
            data_types
        """
        return self.configs['data_types']

    @property
    def percentage_outliers_options(self):
        """
        Gets the percentage_outliers_options from the file

        return:
            percentage_outliers_options
        """
        return self.configs['percentage_outliers_options']

    @property
    def data_sizes(self):
        """
        Gets the data_sizes from the file

        return:
            data_sizes
        """
        return self.configs['data_sizes']


class YamlConfigurationManager(ConfigurationManager):
    """
    Concrete class to implement the abstract class when it is yaml file

    methods:
        read
    """

    def read(self):
        """
        read yaml file

        return:
            data
        """
        with open(self.source) as f:
            data = yaml.safe_load(f)

        return data


class JsonConfigurationManager(ConfigurationManager):
    def read(self):
        """
        read json file

        return:
            data
        """
        with open(self.source) as f:
            jsondata = f.read()
            data = json.loads(jsondata)

            date_str = data['start_date']
            date_format = '%Y-%m-%d'
            date_obj = datetime.strptime(date_str, date_format)
            data['start_date'] = date_obj

        return data
