from datetime import datetime
import os
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


UPLOAD_FOLDER = 'PDFs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/download/<filename>')
def download_file(filename):
    return redirect(url_for('static', filename=os.path.join(app.config['UPLOAD_FOLDER'], filename)))


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'pdf-upload' not in request.files:
        return 'No file part'
    
    file = request.files['pdf-upload']
    
    if file.filename == '':
        return 'No selected file'
    
    if file and file.filename.endswith('.pdf'):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return 'File successfully uploaded and saved'
    
    return 'Invalid file type. Only PDF files are allowed.'

@app.route('/files')
def list_files():
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'name')  # Default to sorting by name

    # Get list of PDF files and their metadata
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.pdf'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_info = {
                'name': filename,
                'date': datetime.fromtimestamp(os.path.getmtime(file_path))
            }
            files.append(file_info)

    # Filter by search query
    if search_query:
        files = [f for f in files if search_query.lower() in f['name'].lower()]

    # Sort files
    if sort_by == 'name':
        files.sort(key=lambda x: x['name'].lower())
    elif sort_by == 'date':
        files.sort(key=lambda x: x['date'])

    return render_template('pdfs.html', files=files, search_query=search_query, sort_by=sort_by)
