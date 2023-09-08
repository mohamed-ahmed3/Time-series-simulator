from configuration_manager import ConfigurationManagerCreator, YamlConfigurationManager, JsonConfigurationManager
import unittest
from unittest.mock import patch


class TestConfigurationManager(unittest.TestCase):
    """
    Unit tests for the ConfigurationManager and its subclasses.

    These tests check the creation of configuration manager instances based on different sources
    (YAML, JSON) and verify that an exception is raised when an unknown source is provided.
    """
    @patch.multiple(ConfigurationManagerCreator, __abstractmethods__=set())
    def setUp(self) -> None:
        """
        Set up common test data.
        """
        self.source_yml = "example.yml"
        self.source_json = "example1.json"

    def test_create_yaml(self):
        """
        Test the successful creation of a YAML configuration manager instance.
        """
        yaml_instance = ConfigurationManagerCreator.create(self.source_yml)
        self.assertIsInstance(yaml_instance, YamlConfigurationManager)

    def test_create_json(self):
        """
        Test the successful creation of a JSON configuration manager instance.
        """
        json_instance = ConfigurationManagerCreator.create(self.source_json)
        self.assertIsInstance(json_instance, JsonConfigurationManager)

    def test_create_unknown(self):
        """
        Test that an exception is raised when an unknown source is provided.
        """
        with self.assertRaises(Exception):
            ConfigurationManagerCreator.create("example.env")


class TestYamlConfigurationManager(unittest.TestCase):
    """
    Unit tests for the YamlConfigurationManager class.

    These tests verify the functionality of the YamlConfigurationManager class, including
    reading configuration data successfully and accessing the 'start_date' attribute.
    """
    def setUp(self) -> None:
        """
        Set up the test environment by creating a YamlConfigurationManager instance.
        """
        self.source_yml = ConfigurationManagerCreator.create("example.yml")

    def test_read(self):
        """
        Test the successful reading of configuration data from a YAML source.
        """
        data = self.source_yml.read()
        self.assertIsInstance(data, dict)

    def test_start_date(self):
        """
        Test accessing the 'start_date' attribute of the YamlConfigurationManager.
        """
        data = self.source_yml.read()
        date = self.source_yml.start_date

        self.assertEqual(date, data['start_date'])


class TestJsonConfigurationManager(unittest.TestCase):
    """
    Unit tests for the JsonConfigurationManager class.

    These tests verify the functionality of the JsonConfigurationManager class, including
    reading configuration data successfully and accessing the 'start_date' attribute.
    """
    def setUp(self) -> None:
        """
        Set up the test environment by creating a JsonConfigurationManager instance.
        """
        self.source_json = ConfigurationManagerCreator.create("example1.json")

    def test_read(self):
        """
        Test the successful reading of configuration data from a JSON source.
        """
        data = self.source_json.read()
        self.assertIsInstance(data, dict)

    def test_start_date(self):
        """
        Test accessing the 'start_date' attribute of the JsonConfigurationManager.
        """
        data = self.source_json.read()
        date = self.source_json.start_date

        self.assertEqual(date, data['start_date'])


if __name__ == '__main__':
    unittest.main()
