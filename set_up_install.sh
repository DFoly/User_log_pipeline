#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS="/Users/danielfoley/desktop/blog/GCP_user_logs/pipeline_scripts/gcpkeys.json"
export PROJECT="user-logs-237110"
export BUCKET="gs://macbook_files"


apt-get install python-pip
sudo pip install apache-beam[gcp] oauth2client==3.0.0 
sudo pip install -U pip
sudo pip install Faker==1.0.2