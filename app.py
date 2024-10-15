from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Ensure the text file exists in the root directory
file_path = os.path.join(os.getcwd(), 'form-data.txt')
max_entries = 20  

# Endpoint to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Format the new entry data
    new_entry = f"Name: {name}\nEmail: {email}\nMessage: {message}\n\n"

    try:
        # Read the current file content
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                existing_data = f.read().strip().split('\n\n')
        else:
            existing_data = []

        # Append new entry to the existing data
        existing_data.append(new_entry.strip())

        # Check if the total number of entries exceeds the limit
        if len(existing_data) > max_entries:
            # Keep only the last 20 entries
            existing_data = existing_data[-max_entries:]

        # Write the updated data back to the file
        with open(file_path, 'w') as f:
            f.write('\n\n'.join(existing_data) + '\n\n')

        return jsonify({'message': 'Form data saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve the HTML form (static files)
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Create the text file if it doesn't exist
    if not os.path.exists(file_path):
        open(file_path, 'w').close()
    
    app.run(debug=True)