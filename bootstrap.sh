#!/bin/bash
set -euxo pipefail

apt-get update
apt-get install -y git python3-pip python3-venv

cd /opt
rm -rf flaskapp4gcp
git clone https://github.com/fh-swf-hgi/flaskapp4gcp.git
cd flaskapp4gcp

python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install Flask google-cloud-storage pyopenssl

mkdir -p uploads

echo "Bootstrap abgeschlossen"
