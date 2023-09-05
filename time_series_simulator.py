import random

from configuration_manager import ConfigurationManager, ConfigurationManagerCreator
from data_simulator import DataSimulator
from data_producer import DataProducer

random.seed(22)


def main():
    configuration_manager = ConfigurationManagerCreator.create("example.yml")
    data_simulator = DataSimulator(configuration_manager)
    meta_data_producer = DataProducer.create('sample_datasets/meta_data.csv')

    meta_data = []
    for (data, meta_data_point) in data_simulator.generate():
        DataProducer.create(f"sample_datasets/{meta_data_point['id']}").produce(data)
        meta_data.append(meta_data_point)

    meta_data_producer.produce(meta_data)


if __name__ == "__main__":
    main()
