"""
Counter API Implementation
"""
from flask import Flask, jsonify
from . import status

app = Flask(__name__)

COUNTERS = {}

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED
  
def counter_exists(name):
  """Check if counter exists"""
  return name in COUNTERS

@app.route('/counters/<name>', methods=['DELETE'])
def prevent_delete_nonexistent_counter(name):
	"""Prevent deleting a non-existent counter"""
	counter = COUNTERS.pop(name, None)
	
	if counter is None:
		return jsonify({"error": f"Counter {name} not found."}), status.HTTP_404_NOT_FOUND

	return jsonify({"message": f"Counter {name} deleted."}), status.HTTP_200_OK

