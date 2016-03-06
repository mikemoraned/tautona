# Motivation

Playing with extracting knowledge from slack metadata. For example, try to find something out about channels
or people by looking at how they are related on slack.

# Prerequisites

* python3, virtualenv, pip
* a slack api token (your-api-token below)

# Install

    virtualenv venv
    source ./venv/bin/activate

    pip install -r requirements.txt

# Usage

    python3 crawl.py --token your-api-token --distance 0.7 --out crawl.json
    python3 visualise.py --in crawl.json --out vis.json
    python3 -m http.server 8000
    open http://localhost:8000
