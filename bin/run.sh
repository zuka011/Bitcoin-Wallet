#!/bin/bash

pip install -e . > /dev/null

uvicorn app.runner.web.main:app --reload
