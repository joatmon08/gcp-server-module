import os
import json
import pytest
import test_terraform
from network import NetworkFactoryModule
from tags import StandardTags
from server import ServerFactoryModule

expected_server_name = 'hello-world'
expected_environment = 'testing'
expected_network = NetworkFactoryModule(expected_server_name)
expected_tags = StandardTags(expected_environment)

CONFIGURATION_FILE = 'main.tf.json'


def generate_json():
    server = ServerFactoryModule(expected_server_name,
                                 expected_environment,
                                 expected_network,
                                 expected_tags.tags)
    resources = {
        'resource': expected_network.build() + server.build()
    }
    with open(CONFIGURATION_FILE, 'w') as outfile:
        json.dump(resources, outfile, sort_keys=True, indent=4)


@pytest.fixture(scope='session')
def apply_changes(request):

    def destroy():
        test_terraform.destroy()
        os.remove(CONFIGURATION_FILE)

    request.addfinalizer(destroy)

    generate_json()

    assert os.path.exists(CONFIGURATION_FILE)
    ret, _, _ = test_terraform.initialize()
    assert ret == 0

    return test_terraform.apply()


@pytest.mark.integration
def test_changes_have_successful_return_code(apply_changes):
    return_code = apply_changes[0]
    assert return_code == 0


@pytest.mark.integration
def test_changes_should_have_no_errors(apply_changes):
    errors = apply_changes[2]
    assert errors == b''


@pytest.mark.integration
def test_changes_should_complete(apply_changes):
    changes = apply_changes[1].decode(encoding='utf-8').split('\n')
    status = test_terraform.status(changes)
    assert 'Apply complete!' in status
