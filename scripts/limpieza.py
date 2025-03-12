import pandas as pd
import numpy as np
import os
import csv
import time

ini = time.time_ns()

def load_data():
    print("Cargando datos")
    i = 0
    with open("../data/220720COVID19MEXICO.csv", "r", encoding="utf-8") as file:
        data_reader = csv.reader(file)
        # Print metadata of first row
        metadata = next(data_reader)
        print(metadata)
        for row in data_reader:
            if(i%1000000 == 0):
                print(i, row)
            i += 1
        print(f"Total de registros: {i}")
        
    print("Datos cargados")

load_data()

fin = time.time_ns()

print(f"Tiempo de ejecución: {(fin-ini)/1e9} segundos")


