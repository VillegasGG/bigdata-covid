import pandas as pd
import numpy as np
import os
import csv
import time
import pickle

ini = time.time_ns()

METADATA_LEN = 40

def adding_new_row_to_csv(row, file_path):
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(row)

def detect_missing_extra_fields(row):
    if len(row) != METADATA_LEN:
        print(f"Error en registro: {row}, len: {len(row)}")
        adding_new_row_to_csv(row, "../data/error_len.csv")
        return True
    return False

def load_and_find_errors():
    print("Cargando datos")
    field_types = open_dict("../data/metadata_types_generated.pkl")
    print("Tipos de campos cargados")
    print(f'field_types: {field_types}')
    errores = 0
    i = 0
    with open("../data/220720COVID19MEXICO.csv", "r", encoding="utf-8") as file:
        data_reader = csv.reader(file)
        # Print metadata of first row
        metadata = next(data_reader)
        print(metadata)
        for row in data_reader:
            error = detect_missing_extra_fields(row)
            if error:
                errores += 1
                print(i, row)
            i += 1
        print(f"Total de registros: {i}")
        print(f"Total de errores: {errores}")
        
    print("Datos cargados")

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


