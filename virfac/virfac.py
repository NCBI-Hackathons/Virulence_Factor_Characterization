# -*- coding: utf-8 -*-

"""Main module."""

import os, os.path


data_dir = os.path.join(os.path.expanduser('~'), '.virfac', 'fasta_data')
os.makedirs(data_dir, exist_ok=True)