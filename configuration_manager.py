from abc import ABC, abstractmethod
import sqlite3

import yaml
import json
from datetime import datetime


class ConfigurationManagerCreator:
    def __init__(self, source: str):
        """
        Initializes the configuration manager instance.

        Parameters:
            source: The source of the data. Can be yaml file or json file
        """
        self.source = source

    @classmethod
    def create(cls, source: str, simulator_name):
        """
        Creates an instance from the chosen source.

        Parameters:
            source: The source of the data. Can be yaml file or json file

        """
        if source.endswith('.yml'):
            return YamlConfigurationManager(source)

        elif source.endswith('.json'):
            return JsonConfigurationManager(source)

        elif source.endswith('.sqlite3'):
            return DatabaseReader(source, simulator_name)

        else:
            raise Exception(f"Unsupported source: {source}")


class ConfigurationManager(ABC):
    """
    An abstract class that provides a configuration manager framework.
    methods:
        __init__: Initializes the configuration manager instance.
        create: Factory method to create an instance of a specific configuration manager.
        read: Abstract method for reading configuration data from a source.

    """

    def __init__(self, source: str):
        """
        Initializes the configuration manager instance.

        Parameters:
            source: The source of the data. Can be yaml file or json file
        """
        self.source = source
        self.configs = self.read()

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


class DatabaseReader(ConfigurationManager):
    def __init__(self, source, simulator_name):
        self.source = source
        self.simulator_name = simulator_name
        self.configs = self.read()

    def read(self):

        conn = sqlite3.connect(self.source)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM simulator_api_simulator WHERE name=?", (self.simulator_name,))
        simulator_row = cursor.fetchone()

        if simulator_row is None:
            cursor.close()
            conn.close()
            return

        simulator_columns = [desc[0] for desc in cursor.description]

        if simulator_columns is None:
            cursor.close()
            conn.close()
            return
        simulator_data = dict(zip(simulator_columns, simulator_row))

        cursor.execute("SELECT * FROM simulator_api_configuration WHERE simulator_id=?",
                       (simulator_data['process_id'],))

        configurations_rows = cursor.fetchall()

        configurations_columns = [desc[0] for desc in cursor.description]
        configurations_data = [dict(zip(configurations_columns, row)) for row in configurations_rows]

        frequencies = [config_data['frequency'] for config_data in configurations_data]
        noise_level = [config_data['noise_level'] for config_data in configurations_data]
        trends = [config_data['trend_coefficients'] for config_data in configurations_data]
        cycles = [config_data['cycle_component_frequency'] for config_data in configurations_data]
        outliers = [config_data['outlier_percentage'] for config_data in configurations_data]

        for config_data in configurations_data:
            cursor.execute("SELECT * FROM simulator_api_seasonalitycomponentdetails WHERE config_id=?",
                           (config_data['id'],))
            seasonality_rows = cursor.fetchall()

            seasonality_columns = [desc[0] for desc in cursor.description]
            seasonality_data = [dict(zip(seasonality_columns, row)) for row in seasonality_rows]

            daily_seasonality_options = []
            weekly_seasonality_options = []

            for season_data in seasonality_data:
                if season_data['frequency_type'] == 'Daily':
                    daily_seasonality_options.append("exist")
                    weekly_seasonality_options.append("none")

                elif season_data['frequency_type'] == 'Weekly':
                    daily_seasonality_options.append("none")
                    weekly_seasonality_options.append("exist")

            config_data['seasonality_components'] = seasonality_data
        cursor.close()
        conn.close()

        simulator_data['configurations'] = configurations_data
        simulator_data['frequencies'] = frequencies
        simulator_data['daily_seasonality_options'] = daily_seasonality_options
        simulator_data['weekly_seasonality_options'] =weekly_seasonality_options
        simulator_data['noise_levels'] = noise_level
        simulator_data['trend_levels'] = trends
        simulator_data['cyclic_periods'] = cycles
        simulator_data['percentage_outliers_options'] = outliers

        return (simulator_data)