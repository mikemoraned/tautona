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

## Get base information

    python3 crawl.py --token your-api-token --distance 0.7 --out crawl.json

## Visualise channel similarity

    python3 visualise.py --in crawl.json --out vis.json
    python3 -m http.server 8000
    open http://localhost:8000
    
## Recommend channels

    Assuming some user-name:

    python3 recommend.py --token your-api-token --in crawl.json --user user-name
