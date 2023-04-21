### Code taken from: Miguel Grinberg - "Handling File Uploads With Flask"
### https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename

# Uncomment when using Cloud Storage
#from google.cloud import storage

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

# Set True when using Cloud Storage
app.config['LOCAL_STORAGE'] = True

# Provide Bucket Name when using Cloud Storage
app.config['BUCKET_NAME'] = 'Your bucket name here'

def list_blobs(bucket_name):
    """
    Objekte in einem Bucket auflisten:
    https://cloud.google.com/storage/docs/listing-objects?hl=de#storage-list-objects-python
    """
    pass

def upload_obj(bucketname, dateiname, zielname=None):
    """
    Datei in einen Bucket hochladen
    https://cloud.google.com/storage/docs/uploading-objects?hl=de#storage-upload-object-python
    Hint: Use 'upload_from_string' as the file content is sent via a POST request:
    https://stackoverflow.com/questions/70116860/upload-file-to-cloud-storage-from-request-without-saving-it-locally
    """
    pass


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
def index():
    if app.config['LOCAL_STORAGE']:
        files = os.listdir(app.config['UPLOAD_PATH'])
    else:
        files = [f.name for f  in list_blobs(app.config['BUCKET_NAME'])]
    return render_template('index.html', files=files)
 
@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400)
        if app.config['LOCAL_STORAGE']:
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        else:
            upload_obj(app.config['BUCKET_NAME'], uploaded_file,  filename)
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
  

if __name__ == "__main__":
    app.run(host="0.0.0.0")
