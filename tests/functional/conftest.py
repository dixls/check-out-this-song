import pytest

@pytest.fixture
def bytes_bjork():
    return b"bj\xc3\xb6rk"

@pytest.fixture
def bytes_bjork_capitalized():
    return b"Bj\xc3\xb6rk"