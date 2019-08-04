from nose.tools import *


def setup():
    print('SETUP')


def teardown():
    print('tear down!')


def test_basic():
    print('I Ran!', end='')
