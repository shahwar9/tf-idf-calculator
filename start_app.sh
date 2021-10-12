#!/bin/bash

conda init bash
conda activate tfidf
export FLASK_APP=app
export FLASK_ENV=development

python app.py
