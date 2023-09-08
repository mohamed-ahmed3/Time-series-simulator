import random

from configuration_manager import ConfigurationManagerCreator
from data_simulator import DataGenerator
from data_producer import DataProducerFileCreation

random.seed(22)


def main():
    configuration_manager = ConfigurationManagerCreator.create("example.yml")
    data_simulator = DataGenerator(configuration_manager)
    meta_data_producer = DataProducerFileCreation.create('sample_datasets/meta_data.csv')

    meta_data = []
    for (data, meta_data_point) in data_simulator.generate():
        DataProducerFileCreation.create(f"sample_datasets/{meta_data_point['id']}").produce(data)
        meta_data.append(meta_data_point)

    meta_data_producer.produce(meta_data)


if __name__ == "__main__":
    main()
