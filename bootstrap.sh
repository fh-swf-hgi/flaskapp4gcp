#!/bin/bash
set -euxo pipefail

apt-get update
apt-get install -y git python3-pip python3-venv

APP_DIR=/opt/flaskapp4gcp

cd /opt
rm -rf "$APP_DIR"
git clone https://github.com/fh-swf-hgi/flaskapp4gcp.git "$APP_DIR"
cd "$APP_DIR"

python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install Flask google-cloud-storage pyopenssl

mkdir -p "$APP_DIR/uploads"
chmod -R a+rX "$APP_DIR"
chmod -R a+rwX "$APP_DIR/uploads"

cat > /etc/profile.d/flaskapp.sh <<EOF
cd /opt/flaskapp4gcp
source /opt/flaskapp4gcp/venv/bin/activate
EOF

chmod +x /etc/profile.d/flaskapp.sh

echo "Bootstrap abgeschlossen"
