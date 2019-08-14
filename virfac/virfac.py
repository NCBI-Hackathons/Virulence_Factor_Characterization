# -*- coding: utf-8 -*-

"""Main module."""

import os, os.path


data_dir = os.environ.get('DATA_DIR', os.path.join(os.path.expanduser('~'), '.virfac', 'data'))
os.makedirs(data_dir, exist_ok=True)