from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from config import config
from parse_csv import ParseCsv


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), config['input_folder_path'])
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), config['output_folder_path'])

ALLOWED_EXTENSIONS = ['.csv']

app = Flask(__name__)
# app.config['ENV'] = 'development'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER



def allowed_file(filename):
    return os.path.splitext(filename)[-1] in ALLOWED_EXTENSIONS

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/processed/<filename>')
def uploaded_file(filename):
    filename_without_ext = os.path.splitext(filename)[0]
    outputfilename = filename_without_ext+'.json'
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], outputfilename, as_attachment =True)


@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('You have not selected a file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        p1 = ParseCsv(filename=filename, headers=True)

        try:
            p1.process()
        except Exception as e:
            print(str(e))
            flash('File does not have a valid format')

        return redirect(url_for('uploaded_file', filename=filename))

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    # host='0.0.0.0'