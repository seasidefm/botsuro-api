#!/bin/bash

pm2 start "poetry run uvicorn main:app --port 8081" --name botsuro-api