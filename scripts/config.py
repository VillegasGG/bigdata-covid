# config.py
# Configuration file for the COVID-19 analysis project.
# All file paths, column names, and settings are defined here.

from pathlib import Path

# --- FILE PATHS ---
# Base directory of the project. This makes the script portable.
BASE_DIR = Path(__file__).parent.resolve()

# Input data file path (assuming data is in a 'data' subdirectory)
# !!! IMPORTANT !!!
# You MUST place your '220720COVID19MEXICO.csv' file inside a folder
# named 'data' in the same directory as these python scripts.
# Project structure should be:
# /your_project_folder
#   - main.py
#   - analysis.py
#   - plotting.py
#   - config.py
#   - /data
#     - 220720COVID19MEXICO.csv
DATA_FILE_PATH = BASE_DIR / "data" / "220720COVID19MEXICO.csv"

# --- ENTITY CATALOG FILE ---
# Path to the Excel file containing entity names and codes.
# Place this file in the 'data' subfolder as well.
CATALOG_FILE_NAME = "201128 Catalogos.xlsx"  # <--- UPDATE THIS FILENAME
CATALOG_FILE_PATH = BASE_DIR / "data" / CATALOG_FILE_NAME
CATALOG_SHEET_NAME = 'Catálogo de ENTIDADES'
CATALOG_KEY_COL = 'CLAVE_ENTIDAD'
CATALOG_VALUE_COL = 'ENTIDAD_FEDERATIVA'


# Directory to save output images and reports
OUTPUT_DIR = BASE_DIR / "results"

# --- DATA PROCESSING SETTINGS ---
# The number of rows to read from the CSV file at a time.
# Adjust this based on your system's memory (RAM).
CHUNK_SIZE = 5_000_000

# --- COLUMN MAPPINGS (Main Data) ---
# It is critical that these names exactly match the headers in your CSV file.
ENTITY_COL = 'ENTIDAD_UM'
RESULT_LAB_COL = 'RESULTADO_LAB'
RESULT_ANT_COL = 'RESULTADO_ANTIGENO'
FINAL_RESULT_COL = 'CLASIFICACION_FINAL'


# --- RESULT DEFINITIONS ---
# Defines which values in the 'CLASIFICACION_FINAL' column are considered positive or negative.
# 1, 2, 3 = Confirmed positive cases
POSITIVE_VALUES = [1, 2, 3]
# 7 = Negative case
NEGATIVE_VALUE = 7
