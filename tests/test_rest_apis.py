import os

import pytest
from app import create_app


@pytest.fixture
def client():
    os.environ["{}_env"] = "testing"
    client = create_app().test_client()
    yield client
