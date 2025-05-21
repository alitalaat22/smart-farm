#!/bin/bash
source venv/bin/activate
gunicorn --bind 0.0.0.0:80 farm_system:app
