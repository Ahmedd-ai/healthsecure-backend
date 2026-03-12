"""
WSGI entry point for deployment on Render.
This file is used by Gunicorn to serve the FastAPI application.
"""

from main import app

# This is required for Gunicorn to find the app
# The variable must be named 'app' as per Procfile: wsgi:app
