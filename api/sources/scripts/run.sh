#!/usr/bin/env bash
echo "Launch API: Start"
. /container/venv/bin/activate
sleep 10
uvicorn --host ${HTTP_HOST} --port ${HTTP_PORT} api.app:app
