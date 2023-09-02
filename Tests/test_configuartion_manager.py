from configuration_manager import ConfigurationManager, YamlConfigurationManager, JsonConfigurationManager
import unittest
from unittest.mock import patch


class TestConfigurationManager(unittest.TestCase):
    @patch.multiple(ConfigurationManager, __abstractmethods__=set())
    def setUp(self) -> None:
        self.source_yml = "example.yml"
        self.source_json = "example1.json"

    def test_create_yaml_success(self):
        yaml_instance = ConfigurationManager.create(self.source_yml)
        self.assertIsInstance(yaml_instance, YamlConfigurationManager)

    def test_create_json_success(self):
        json_instance = ConfigurationManager.create(self.source_json)
        self.assertIsInstance(json_instance, JsonConfigurationManager)

    def test_create_unknown_success(self):
        with self.assertRaises(Exception):
            ConfigurationManager.create("example.env")


class TestYamlConfigurationManager(unittest.TestCase):
    def setUp(self) -> None:
        self.source_yml = ConfigurationManager.create("example.yml")

    def test_read_success(self):
        data = self.source_yml.read()
        self.assertIsInstance(data, dict)

    def test_start_date_success(self):
        data = self.source_yml.read()
        date = self.source_yml.start_date

        self.assertEqual(date, data['start_date'])


class TestJsonConfigurationManager(unittest.TestCase):
    def setUp(self) -> None:
        self.source_json = ConfigurationManager.create("example1.json")

    def test_read_success(self):
        data = self.source_json.read()
        self.assertIsInstance(data, dict)

    def test_start_date_success(self):
        data = self.source_json.read()
        date = self.source_json.start_date

        self.assertEqual(date, data['start_date'])


if __name__ == '__main__':
    unittest.main()
