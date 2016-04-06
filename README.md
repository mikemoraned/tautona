# Motivation

Playing with extracting knowledge from slack metadata. For example, try to find something out about channels
or people by looking at how they are related on slack.

# Prerequisites

* python3, virtualenv, pip
* a slack api token (API_TOKEN below)

# Install

    virtualenv venv
    source ./venv/bin/activate

    pip install -r requirements.txt

# Usage

## Setup defaults

    export API_TOKEN="your-api-token"

## Get base information

Only include those channels written to in last 3 months, and with a Jaccard distance of 0.7 or less

    TS=$(date -v-3m +%s) python3 crawl.py --token $API_TOKEN --distance 0.7 --recency $TS --out crawl.json

## Visualise channel similarity

    python3 visualise.py --in crawl.json --out vis.json
    python3 -m http.server 8000
    open http://localhost:8000
    
## Recommend channels

    Assuming some user-name:

    python3 recommend.py --token $API_TOKEN --in crawl.json --user user-name
