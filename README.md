# plex-telegram-notify

## Introduction
Simple python script for plex web hooks to send notifications over telegram. Just change the config variables in run.py to your telegram-bot (created with botfather). You can run the script directly with python or with the provided docker files as a container.

## Install
* Change config variables in run.py to your environment
* docker build -t plex-webhook .
* docker compose up -d
