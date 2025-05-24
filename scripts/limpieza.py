import pandas as pd
import numpy as np
import os
import csv
import time
import pickle
from origen import validate_origen
from sector import validate_sector
from tqdm import tqdm

ini = time.time_ns()

METADATA_LEN = 40

def adding_new_row_to_csv(row, file_path):
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(row)

def detect_missing_extra_fields(row):
    if len(row) != METADATA_LEN:
        adding_new_row_to_csv(row, "../data/error_len.csv")
        return True
    return False

def save_error_row(row, file_path):
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(row)

def show_final_errors(length_errors, origen_errors, sector_errors):
    print(f"Total de errores: {length_errors}")
    print(f"Total de errores en origen: {origen_errors}")
    print(f"Total de errores en sector: {sector_errors}")

def load_and_find_errors():
    print("Cargando datos")
    origen_errors = 0
    sector_errors = 0
    errores = 0
    i = 0
    with open("../data/220720COVID19MEXICO.csv", "r", encoding="utf-8") as file:
        data_reader = csv.reader(file)
        # Print metadata of first row
        metadata = next(data_reader)
        is_origen_error = False
        is_sector_error = False
        print(metadata)
        for row in tqdm(data_reader):
            is_origen_error = validate_origen(row)
            is_sector_error = validate_sector(row)
            error = detect_missing_extra_fields(row)
            if error:
                errores += 1
                # print(i, row)
            i += 1

            if is_origen_error:
                # save origen errors in a txt file
                save_error_row(row, "../data/error_origen.txt") 
                origen_errors += 1

            if is_sector_error:
                # save sector errors in a txt file
                save_error_row(row, "../data/error_sector.csv")
                sector_errors += 1

        print(f"Total de registros: {i}")
        show_final_errors(errores, origen_errors, sector_errors)

def open_dict(file_path):
    with open(file_path, 'rb') as file:
        dic = pickle.load(file)
        return dic

def main():
    ini = time.time_ns()
    print("Limpieza de datos")
    load_and_find_errors()
    print("Fin de la limpieza")
    fin = time.time_ns()
    print(f"Tiempo de ejecución: {(fin-ini)/1e9} segundos")


if __name__ == "__main__":
    main()


