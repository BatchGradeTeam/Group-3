"""
Counter API Implementation
"""
from flask import Flask, jsonify
from src import status

# ======================
# Instances

app = Flask(__name__)

# Reusable const for the initial value of a counter.
INITIAL_COUNTER_VALUE = 0

# A dictionary to store the counters, where
#   the key is the counter name, and
#   the value is the counter value.
COUNTERS = {}


# ======================
# Functions

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a new counter with the given name"""

    # This version does not handle duplicate names.
    # We can add that logic when student #2 implements their test case.

    COUNTERS[name] = INITIAL_COUNTER_VALUE
    return jsonify({"name": name, "value": COUNTERS[name]}), status.HTTP_201_CREATED

