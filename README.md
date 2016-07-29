# Motivation

Playing with extracting knowledge from slack data or metadata. For example, try to find similar channels,
based on content.

# Prerequisites

* python3, virtualenv, pip
* a slack api token (API_TOKEN below)
    * see https://api.slack.com/bot-users, specifically https://my.slack.com/services/new/bot

# Install

    virtualenv venv
    source ./venv/bin/activate

    pip3 install -r requirements.txt

# Usage

## Setup defaults

    export API_TOKEN="your-api-token"

## Get base information

Find all messages, for any channels that have between 10 and 1000
recent messages

    python3 crawl.py --token $API_TOKEN

Analyse these messages, extracting what we need for building anything
with them

    python3 analyse.py

## Find similar channels

For a single channel, find top 10 similar channels

    python3 similarity.py --channel some-channel-name --topn 10

## Bulk Convert to channel similarities

Use analysed message content to find similarities between channels, and
convert this similarity to a distance measure, only allowing channels closer
than 0.8.

    python3 similarities.py --distance 0.8 --out content.sims.json

## Visualise channel similarity

Set up vis submodule

    cd vis/
    git submodule init
    git submodule update
    cd ..

Generate visualisation format

    python3 visualise.py --in content.sims.json --out vis/vis.json

Display visualisation (after this step, you rerun generation step and just reload the page)

    cd vis && python3 -m http.server 8000 &
    open http://localhost:8000

If you'd like to share the visualisation, you can just share the contents of the vis/ directory.

If you want to share, but don't want to give away your channel names then try

    python3 visualise.py --in content.sims.json --out vis/vis.json --obfuscate
    
This will replace parts of channel names with a consistent, but arbitrary, replacement
e.g. "my-channel-name" becomes "mazut-duller-toffy".

By default this will look for random replacement words in /usr/share/dict/words, but you can point it to any
file you like

    python3 visualise.py --in content.sims.json --out vis/vis.json --obfuscate --words-file your-words-file


