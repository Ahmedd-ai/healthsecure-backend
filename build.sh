#!/bin/bash
# Build script for Render deployment

# Initialize and update submodules
git submodule update --init --recursive

# Install Python dependencies
pip install -r requirements.txt
