#!/bin/bash

ENV_DIR=".venv"
GEMINI_API_KEY="$1"

source "$ENV_DIR/bin/activate"

python main.py "$GEMINI_API_KEY"