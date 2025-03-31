import csv
import time
import pickle

dict_sector = {1 : "CRUZ ROJA", 2 : "DIF", 3 : "ESTATAL", 4 : "IMSS", 
5: "BIENESTAR", 6 : "ISSTE", 7 : "MUNICIPAL", 8: "PEMEX", 9 : "PRIVADA", 
10 : "SEMAR", 11 : "SEMAR", 12 : "SSA", 13 : "UNIVERSITARIO", 99: "NO ESPECIFICADO"}


def validate_sector(row):
    actual_value = row[3]
    try:
        actual_value = int(actual_value)
        if actual_value not in dict_sector.keys():
            print(f"Error en registro: {row}, value: {actual_value}")
            return True
    except:
        print(f"Error en registro: {row}, value: {actual_value}")
        return True
    
    return False