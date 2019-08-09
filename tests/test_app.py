import pytest
from flaskr import flaskr


@pytest.fixture
def client():
    # flask_app = create_app()
    pass


def setup():
    print('SETUP')


def teardown():
    print('tear down!')


def test_basic():
    print('I Ran!', end='')
