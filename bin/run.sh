#!/bin/bash

pip install -e .

uvicorn app.runner.web.main:app --reload
