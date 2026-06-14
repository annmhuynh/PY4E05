import os
import secrets

BASE_PATH       = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH   = os.path.join(BASE_PATH, "data", "raw")
CLEAN_DATA_PATH = os.path.join(BASE_PATH, "data", "processed")

TEMPLATES_PATH  = os.path.join(BASE_PATH, "templates")
STATIC_PATH     = os.path.join(BASE_PATH, "static")

DEBUG = True
SECRET_KEY = secrets.token_hex(16)