import os
from flask import Flask, render_template, request, jsonify
from utils.processor import rank_resumes

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resumes' not in request.files:
        return jsonify({'error': 'No resume files uploaded'}), 400
    
    job_description = request.form.get('job_description', '')
    if not job_description:
        return jsonify({'error': 'Job description is required'}), 400

    files = request.files.getlist('resumes')
    saved_files = []
    
    # Save files temporarily
    for file in files:
        if file.filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            saved_files.append(file_path)
    
    try:
        results = rank_resumes(job_description, saved_files)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Cleanup uploaded files
        for f in saved_files:
            try:
                os.remove(f)
            except:
                pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
