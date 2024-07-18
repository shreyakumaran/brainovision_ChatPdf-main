import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend import query_engine 

app = Flask(__name__)  # Corrected syntax for Flask app initialization

cors = CORS(app, resources={r"/": {"origins": "*"}})  # Allow all origins for CORS, adjust as needed

# Set the path where uploaded files will be stored
UPLOAD_FOLDER = 'C:\Users\Hp\Downloads\brainovision_ChatPdf-main\brainovision_ChatPdf-main\sample data'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the upload folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    print("uploading file")
    if 'file' not in request.files:
        print('no file found')
        return jsonify({'error': 'No file part'}), 400

    print('file found')
    file = request.files['file']

    if file.filename == '':
        print("no file name")
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        print("saving file")
        # Here you can initialize your RAG or other models with the uploaded file if needed
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

@app.route('/submit', methods=['POST'])
def submit():
    # Process the user request here
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    # Use the query engine from your backend code
    response = query_engine.query(question)
    
    return jsonify({'response': str(response)})

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Ensure the app runs on port 5000 or your desired port
