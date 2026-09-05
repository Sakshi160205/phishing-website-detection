#!/usr/bin/env python
import sys
import json
sys.path.insert(0, '.')

# Import Flask and the app
from flask import Flask, request
import app as app_module

# Create a test client
client = app_module.app.test_client()

# Test the API endpoint
response = client.post('/api/predict', json={'url': 'http://example.com'})
print(f"Status: {response.status_code}")
print(f"Response: {response.json}")
