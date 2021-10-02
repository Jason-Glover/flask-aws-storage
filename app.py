import os
from flask import Flask, render_template, request, redirect, send_file
from s3_functions import create_bucket, filter_bucket, list_bucket, list_files, upload_file, show_image
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
try:
    BUCKET = os.environ['BUCKET_NAME']
except:
    ALLBUCKETS = list_bucket()
    BUCKET = filter_bucket(ALLBUCKETS)
    if BUCKET == None:
        create_bucket()
        BUCKET = list_bucket
        

@app.route("/")
def home():
    contents = list_files(BUCKET)
    return render_template('index.html')

@app.route("/pics")
def list():
    contents = show_image(BUCKET)
    return render_template('collection.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f"uploads/{f.filename}", BUCKET)
        return render_template('index.html')
@app.route('/verify')
def verify():
        return '<p>' + BUCKET + '</p>'

if __name__ == '__main__':
    app.run(debug=True)