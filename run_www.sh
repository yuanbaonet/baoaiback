#!/bin/sh
basepath=$(cd `dirname $0`; pwd)
cd ${basepath}
venv/bin/gunicorn www_manage:app -c deploy/gunicorn_config.py

