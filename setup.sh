#!/usr/bin/env bash
set -e
$(command -v python3) -m venv .venv

source .venv/bin/activate

pip install --upgrade -r requirements.txt