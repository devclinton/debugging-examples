import glob
import json
import logging
from logging import getLogger
import docker

from tests.utils import dump_output

logger = getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_config_object(image='alpine', command='echo hello world', **extra):
    config = dict(
        image=image,
        command=command
    )
    config.update(extra)
    return config


def validate_config(config):
    return len(config) > 0


#@dump_output()
def run_container(config, client=None):
    if client is None:
        client = docker.from_env()
    container = client.create_container(**config)
    return container


def run_hello_world_in_different_flavors_of_linux():
    client = docker.from_env()
    for linux_cfg in glob.glob('*.json'):
        with open(linux_cfg, 'r') as lcfg:
            config = get_config_object(**json.load(lcfg))
            if validate_config(config):
                logger.info(config)
                container = run_container(config, client)
                logger.info(container)
            else:
                logger.warning('Invalid config')



run_hello_world_in_different_flavors_of_linux()