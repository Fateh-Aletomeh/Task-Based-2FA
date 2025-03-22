from flask import Flask, render_template, jsonify, request
import json
import os
import random

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/get-task-data')
def get_task_data():
    """Return the task data from the JSON file."""
    try:
        # Use the same JSON file as your Kivy app
        with open('sample_task_with_named_colors.json', 'r') as file:
            task_data = json.load(file)
        return jsonify(task_data)
    except Exception as e:
        # If the file is not found, return a sample task
        print(f"Error loading task data: {e}")
        return

@app.route('/verify-task', methods=['POST'])
def verify_task():
    """Verify if the submitted circles match the expected response."""
    try:
        data = request.json
        selected_circles = data.get('selectedCircles', [])
        
        # Get the expected response from the task data file
        with open('sample_task_with_named_colors.json', 'r') as file:
            task_data = json.load(file)
        
        expected_response = task_data.get('expectedResponse', [])
        
        # Check if the selected circles match the expected response
        success = (sorted(selected_circles) == sorted(expected_response))
        
        return jsonify({
            'success': success,
            'message': 'Authentication successful!' if success else 'Authentication failed. Selected circles don\'t match.'
        })
    except Exception as e:
        print(f"Error verifying task: {e}")
        return jsonify({
            'success': False,
            'message': f'Error verifying task: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True)