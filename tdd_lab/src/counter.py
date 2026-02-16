"""
Counter API Implementation
"""
from flask import Flask, jsonify
from . import status

app = Flask(__name__)

COUNTERS = {}

def counter_exists(name):
  """Check if counter exists"""
  return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

# ===========================
# Feature: Delete a Counter
# Author: Truc Bui
# Date: 2026-02-15
# Description: Implementation for deleting a counter
# ===========================
@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    """Delete a counter"""
    if counter_exists(name):
        del COUNTERS[name]  # Remove the counter from the dict COUNTERS
        return jsonify({"message": f"Counter {name} has been deleted"}), status.HTTP_204_NO_CONTENT
    # Cannot delete a non-existent counter
    return jsonify({"error": f"Counter {name} does not exist"}), status.HTTP_404_NOT_FOUND
