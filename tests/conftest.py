import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activity_state():
    original_data = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_data)
