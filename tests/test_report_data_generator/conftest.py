import pytest


@pytest.fixture(scope='module')
def popular_words():
    return (('get', 10), ('find', 5), ('set', 8))


