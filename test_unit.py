import pytest
from server import ServerFactoryModule
from network import NetworkFactoryModule
from tags import StandardTags

expected_server_name = 'hello-world'
expected_environment = 'testing'
expected_network = NetworkFactoryModule(expected_server_name)
expected_tags = StandardTags(expected_environment)


@pytest.fixture
def server():
    server = ServerFactoryModule(expected_server_name,
                                 expected_environment,
                                 expected_network,
                                 expected_tags)
    return server.build()[0]['google_compute_instance'][0][
        expected_server_name][0]


@pytest.mark.unit
def test_configuration_for_server_name(server):
    assert server['name'] == expected_server_name


@pytest.mark.unit
def test_configuration_for_subnet_name(server):
    assert server['network_interface'][0]['subnetwork'] == \
        expected_network._subnet_name
