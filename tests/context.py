import sys
from os import path
import os

sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))

try:
    from nosql_versioning import *
except Exception as e:
    print(e)
