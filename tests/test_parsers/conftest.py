import pytest

from codebase_analizer.parsers import CodeBaseParser


@pytest.fixture(scope="module")
def codebase_parser():
    return CodeBaseParser('')
