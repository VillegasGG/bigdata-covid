import csv
import time
import pickle

dict_sector = {1 : "CRUZ ROJA", 2 : "DIF", 3 : "ESTATAL", 4 : "IMSS", 
5: "BIENESTAR", 6 : "ISSTE", 7 : "MUNICIPAL", 8: "PEMEX", 9 : "PRIVADA", 
10 : "SEMAR", 11 : "SEMAR", 12 : "SSA", 13 : "UNIVERSITARIO", 99: "NO ESPECIFICADO"}


def open_dict(file_path):
    with open(file_path, 'rb') as file:
        dic = pickle.load(file)
        return dic

def adding_new_row_to_csv(row, file_path):
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(row)

def detect_sector(row, dict_sector):
    if int(row[3]) not in dict_sector.keys():
        print(f"Error en registro: {row}, value: {row[3]}")
        adding_new_row_to_csv(row, "../data/error_sector.csv")
        return True
    return False
        

def find_error_rows():
    dict_catalogos = open_dict("../data/metadata_types_generated.pkl")
    print(f'field_types: {dict_catalogos[4]}')

    errores = 0
    i = 0
    with open("../data/220720COVID19MEXICO.csv", "r", encoding="utf-8") as file:
        data_reader = csv.reader(file)
        # Print metadata of first row
        metadata = next(data_reader)
        print(metadata)
        for row in data_reader:
            error = detect_sector(row, dict_sector)
            if error:
                errores += 1
            if(i%1000000 == 0):
                print(i, row)
            i += 1
        print(f"Total de registros: {i}")
        print(f"Total de errores: {errores}")

def main():
    ini = time.time_ns()
    print("Empieza errores en sector")
    find_error_rows()
    print("Fin de errores en sector")
    fin = time.time_ns()
    print(f"Tiempo de ejecución: {(fin-ini)/1e9} segundos")

if __name__ == "__main__":
    main()