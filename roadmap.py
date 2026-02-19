#!/usr/bin/env python
"""Entry point for the roadmap renderer. Prefer: python -m roadmap"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from roadmap_app.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
