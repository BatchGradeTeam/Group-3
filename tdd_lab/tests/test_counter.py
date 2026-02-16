"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest
from src import app
from src import status

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    # ===========================
    # Test: Create New Counter
    # Author: Tri Tran
    # Date: 2026-02-15
    # Description: Ensure a new counter can be created using
    #   POST /counters/<name> and that it initializes with value 0.
    # ===========================
    def test_create_new_counter(self, client):
        """POST /counters/<name> should create a counter with initial value 0"""

        # send a POST request to create a new counter named "foo"
        result = client.post("/counters/foo")

        # 1. Verify that the status code is 201 Created
        assert result.status_code == status.HTTP_201_CREATED

        # 2. Verify that the result contains the counter name and initial value
        data = result.get_json()    # convert from JSON to a dictionary
        assert data["name"] == "foo"
        assert data["value"] == 0

