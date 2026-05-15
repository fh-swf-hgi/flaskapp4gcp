#!/bin/bash
set -euxo pipefail

apt-get update
apt-get install -y git python3-pip python3-venv python3-google-cloud-storage

cd /opt
git clone https://github.com/fh-swf-hgi/flaskapp4gcp.git
cd flaskapp4gcp

python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install Flask google-cloud-storage pyopenssl

mkdir -p uploads
chown -R "$USER":"$USER" /opt/flaskapp4gcp || true

echo "Bootstrap abgeschlossen"
