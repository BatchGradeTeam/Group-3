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
from flask import jsonify
import pytest
from src import app
from src import status

@pytest.fixture()
def client():
    """Fixture for Flast test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test case for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREAATED

    def test_get_nonexistent_counter(self, client):
        """GET on a non-existent counter should return 404"""
        result = client.get('/counters/nonexistent')
        assert result.status_code == status.HTTP_404_NOT_FOUND

COUNTERS = {}

def counter_exists(name):
    """Check if a counter with the given name exists"""
    return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    if counter_exists(name):
        return jsonify({'error': f"Counter '{name}' already exists."}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

@app.route('/counters/<name>', methods=['GET'])
def non_existen_counter(name):
    if not counter_exists(name):
        return jsonify({'error': f"Counter '{name}' not found."}), status.HTTP_404_NOT_FOUND
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK