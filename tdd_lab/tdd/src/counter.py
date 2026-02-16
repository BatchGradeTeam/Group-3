"""Counter API Implementation"""
from flask import Flask, jsonify
from . import status

app = Flask(__name__) 