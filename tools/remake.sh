#!/bin/bash
set -e
cd "$(dirname "$0")/.."

APPS="user form org attachment audit template"

remake() {
    sudo mysql < tools/remake.sql
    rm -rf ./*/migrations
    python manage.py makemigrations $APPS
    python manage.py migrate
}

remake
