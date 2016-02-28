# Motivation

Playing with extracting knowledge from slack metadata. For example, try to find something out about channels
or people by looking at how they are related on slack.

# Prerequisites

* python3, virtualenv, pip
* on mac you also need brew
* a slack api token (your-api-token below)

# Install

    virtualenv venv
    source ./venv/bin/activate

    # on mac, you also need:
    brew install libffi

    pip install -r requirements.txt

# Usage

    python3 --token your-api-token --size 20 --out summary.json
    python3 -m http.server 8000
    open http://localhost:8000
