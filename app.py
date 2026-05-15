import argparse
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename

# Default-Konfiguration
DEFAULT_USE_CLOUD_STORAGE = False
DEFAULT_BUCKET_NAME = "fhkuerzel-imagebucket"
DEFAULT_UPLOAD_DIR = "uploads"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
MAX_UPLOAD_SIZE = 10 * 1024 * 1024


# Kommandozeilenparameter
parser = argparse.ArgumentParser()
parser.add_argument("--cloud-storage", action="store_true")
parser.add_argument("--bucket", default=DEFAULT_BUCKET_NAME)
parser.add_argument("--upload-dir", default=DEFAULT_UPLOAD_DIR)

args = parser.parse_args()

USE_CLOUD_STORAGE = args.cloud_storage
BUCKET_NAME = args.bucket
UPLOAD_DIR = Path(args.upload_dir)


if USE_CLOUD_STORAGE:
    from google.cloud import storage
    storage_client = storage.Client()
else:
    UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE


def validate_image(file):
    header = file.read(10)
    file.seek(0)

    if header.startswith(b"\xff\xd8"):
        return ".jpg"

    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"

    if header[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"

    return None


def list_files():
    if USE_CLOUD_STORAGE:
        bucket = storage_client.bucket(BUCKET_NAME)
        return [blob.name for blob in storage_client.list_blobs(bucket)]

    return [
        p.name for p in UPLOAD_DIR.iterdir()
        if p.suffix.lower() in ALLOWED_EXTENSIONS
    ]


def save_file(file, filename):
    if USE_CLOUD_STORAGE:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)

        blob.upload_from_file(
            file,
            content_type=file.content_type,
            rewind=True
        )
    else:
        file.save(UPLOAD_DIR / filename)


def get_file(filename):
    if USE_CLOUD_STORAGE:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)

        if not blob.exists():
            abort(404)

        return send_file(
            blob.open("rb"),
            mimetype=blob.content_type or "application/octet-stream",
            download_name=filename
        )

    path = UPLOAD_DIR / filename

    if not path.exists():
        abort(404)

    return send_file(path)


@app.route("/")
def index():
    return render_template("index.html", files=list_files())


@app.route("/", methods=["POST"])
def upload():
    file = request.files.get("file")

    if file is None or file.filename == "":
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    suffix = Path(filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        abort(400)

    if validate_image(file.stream) is None:
        abort(400)

    save_file(file, filename)

    return redirect(url_for("index"))


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return get_file(filename)


if __name__ == "__main__":
    print(f"Cloud Storage: {USE_CLOUD_STORAGE}")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Upload Directory: {UPLOAD_DIR}")

    app.run(host="0.0.0.0", port=5000)
