#!/bin/bash

ENV_DIR=".venv"
REQ_FILE="requirements.txt"

python3 -m venv "$ENV_DIR"
source "$ENV_DIR/bin/activate"
pip install --upgrade pip setuptools wheel
pip install --no-cache-dir -r "$REQ_FILE" --default-timeout=1000