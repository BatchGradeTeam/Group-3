# from flask import Flask

# app = Flask(__name__)

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

#  counter creation check helper function
def counter_exists(name):
  """Check if counter exists"""
  return name in COUNTERS

@app.route('/counters/reset', methods=['POST'])
def reset_counters():
    """Reset all counters"""
    COUNTERS.clear()
    return jsonify({"message": "All counters have been reset"}), status.HTTP_200_OK



