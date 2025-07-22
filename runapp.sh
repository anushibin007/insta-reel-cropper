#!/bin/sh

python -m streamlit run app.py --browser.gatherUsageStats=false --server.port=8501 --server.address=0.0.0.0
