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

APP_DIR=/opt/flaskapp4gcp
APP_USER=$(getent passwd 1000 | cut -d: -f1)
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

cat >> /home/$APP_USER/.bashrc <<EOF

cd /opt/flaskapp4gcp
source /opt/flaskapp4gcp/venv/bin/activate
EOF

echo "Bootstrap abgeschlossen"
