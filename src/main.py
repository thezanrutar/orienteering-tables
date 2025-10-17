#!/usr/bin/env python3
"""
Entry point for the Orienteering Tables application.
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import run_app

if __name__ == '__main__':
    run_app()
