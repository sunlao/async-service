from pytest import fixture
from src.helpers.queue.client import Client


@fixture(scope="module")
def queue_client():
    return Client()


@fixture(scope="module")
def queue_keys():
    return Client().keys()


@fixture(scope="module")
def queue_health():
    return Client().health()
