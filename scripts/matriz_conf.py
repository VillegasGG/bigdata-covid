import csv
import os
import time
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics

#dict_final = {[1,2,3] : "Positiva", 7 : "Negativa", [4,5,6] : "Sin Muestra"}
#dict_res_lab = {"1": "positivo", "2" : "negativo"}
#dict_res_ant = {"1": "positivo", "2" : "negativo"}

global dict_ent, actual_total, predicted_total
global VP, FP, FN, VN
dict_ent = {x: [0,0,0,0] for x in range(1,33)}
dict_ent[36] = [0,0,0,0]
dict_ent[97] = [0,0,0,0]
dict_ent[98] = [0,0,0,0]
dict_ent[99] = [0,0,0,0]

actual_total = []
predicted_total = []

dict_ent_actual = {x: [] for x in range(1,37)}
dict_ent_predicted = {x: [] for x in range(1,37)}

VP = 0
FP = 0
FN = 0
VN = 0

def open_dict(file_path):
    with open(file_path, 'rb') as file:
        dic = pickle.load(file)
        return dic

def adding_new_row_to_csv(row, file_path):
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(row)

def detect_sector(row, dict_sector, index):
    if row[3] not in dict_sector.keys():
        #print(f"Error en registro: {row}, \n value: {row[3]} \n registro {index + 1}")
        adding_new_row_to_csv(row, "../data/error_sector.csv")
        return True
    return False

def add_values_list(act_v, pred_v, entity):
    actual_total.append(act_v)
    predicted_total.append(pred_v)
    dict_ent_actual[entity].append(act_v)
    dict_ent_predicted[entity].append(pred_v)


#comparando antigeno,lab (supuesto) a resultado final (real)
def dectect_resultado(row):
    global VP, VN, FP, FN
    try:
        if int(row[4]) in dict_ent.keys():
            # Verdaderos positivos
            if (row[32] == "1" or row[34] == "1") and row[35] in ["1","2","3"]:
                VP+=1
                dict_ent[int(row[4])][0]+=1

                add_values_list(1,1, int(row[4]))

            # Falsos positivos
            elif (row[32] == "1" or row[34] == "1") and row[35] == "7":
                FP+=1
                dict_ent[int(row[4])][1]+=1

                add_values_list(0,1, int(row[4]))

            # Falsos negativos
            elif (row[32] == "2" or row[34] == "2") and row[35] in ["1","2","3"]:
                FN+=1
                dict_ent[int(row[4])][2]+=1

                add_values_list(1,0, int(row[4]))

            # Verdaderos Negativos
            elif (row[32] == "2" or row[34] == "2") and row[35] == "7":
                VN+=1 
                dict_ent[int(row[4])][3]+=1

                add_values_list(0,0, int(row[4]))
    except:
        print(f"Error en línea {row}")

#final (real) vs anti (supuesto)
def dectect_resultado_anti(row):
    if int(row[4]) in dict_ent.keys():
        # Verdaderos positivos
        if (row[34] == "1") and row[35] in ["1","2","3"]:
            VP+=1
            dict_ent[int(row[4])][0]+=1
            add_values_list(1,1, int(row[4]))

        # Falsos positivos
        elif (row[34] == "1") and row[35] == "7":
            FP+=1
            dict_ent[int(row[4])][0]+=1
            add_values_list(0,1, int(row[4]))

        # Falsos negativos
        elif (row[34] == "2") and row[35] in ["1","2","3"]:
            FN+=1
            dict_ent[int(row[4])][0]+=1
            add_values_list(1,0, int(row[4]))

        # Verdaderos Negativos
        elif (row[34] == "2") and row[35] == "7":
            VN+=1 
            dict_ent[int(row[4])][0]+=1
            add_values_list(0,0, int(row[4]))

#final (real) vs lab (supuesto)
def dectect_resultado_lab(row):
    if int(row[4]) in dict_ent.keys():
        # Verdaderos positivos
        if (row[32] == "1") and row[35] in ["1","2","3"]:
            VP+=1
            dict_ent[int(row[4])][0]+=1
            add_values_list(1,1, int(row[4]))
        # Falsos positivos
        elif (row[32] == "1") and row[35] == "7":
            FP+=1
            dict_ent[int(row[4])][0]+=1
            add_values_list(0,1, int(row[4]))
        # Falsos negativos
        elif (row[32] == "2") and row[35] in ["1","2","3"]:
            FN+=1
            dict_ent[int(row[4])][0]+=1
            add_values_list(1,0, int(row[4]))
        # Verdaderos Negativos
        elif (row[32] == "2") and row[35] == "7":
            VN+=1 
            dict_ent[int(row[4])][0]+=1
            add_values_list(0,0, int(row[4]))

def por_entidad(entidad, directory):
    #print(dict_ent[10][0:5])
    try:
        VP_e = dict_ent[entidad][0]
        FP_e = dict_ent[entidad][1]
        FN_e = dict_ent[entidad][2]
        VN_e = dict_ent[entidad][3]
        accuracy_e = (VP_e + VN_e) / (VP_e + VN_e + FP_e + FN_e)
        specificity_e = VP_e / (VN_e + FP_e)
        sensitivity_e = VP_e / (VN_e + FN_e)

        print(f'accuracy {accuracy_e}')
        print(f'specificity {specificity_e}')
        print(f'sensitivity {sensitivity_e}')

        confusion_matrix_ent = metrics.confusion_matrix(dict_ent_actual[entidad], dict_ent_predicted[entidad])
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix_ent, display_labels = [0, 1])
        cm_display.plot()
        #plt.show()

        filename = 'conf_matrix_' + str(entidad) + '.png'
        filepath = os.path.join(directory, filename) # creates the full path
        plt.savefig(filepath)

        # Close the plot
        plt.close()
    except Exception as e:
        print("nah")
        # Print the exception name
        print(e.__str__()[0:200])
        

def find_matrix():
    dict_catalogos = open_dict("../data/metadata_types_generated.pkl")
    print(f'field_types: {dict_catalogos[4]}')

    with open("../data/220720COVID19MEXICO.csv", "r", encoding="utf-8") as file:
        data_reader = csv.reader(file)
        # Print metadata of first row
        metadata = next(data_reader)
        print(metadata)
        for row in data_reader:
            dectect_resultado(row)

        
        print(f"Total VP: {VP}")
        print(f"Total de VN: {VN}")
        print(f"Total FP: {FP}")
        print(f"Total de FN: {FN}")
    
    accuracy = (VP + VN) / (VP + VN + FP + FN)
    specificity = VP / (VN + FP)
    sensitivity = VP / (VN + FN)

    print(f'--- Resultados país ---')
    print(f'accuracy {accuracy}')
    print(f'specificity {specificity}')
    print(f'sensitivity {sensitivity}')

def main():

    ini = time.time_ns()

    print("Inicia matriz")
    find_matrix()
    
    print("fin calculo")

    directory = '../data/images'
    if not os.path.exists(directory):
        os.makedirs(directory)

    confusion_matrix = metrics.confusion_matrix(actual_total, predicted_total)
    #print(predicted_total[0:10])
    #print(actual_total[0:10])
    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [0, 1])
    print("Hace matriz")
    cm_display.plot()
    #plt.show()
    # Save the plot to a specific directory
    filename = 'conf_matrix_total.png'
    filepath = os.path.join(directory, filename) # creates the full path
    plt.title("Matriz de confusión de México")
    plt.savefig(filepath)
    print("se guardó la figura")
    # Close the plot
    plt.close()

    print("Fin matriz de confusión")

    fin = time.time_ns()

    for key in dict_ent.keys():
        print(f'Para entidad {key}')
        por_entidad(key, directory)

    print(f"Tiempo de ejecución: {(fin-ini)/1e9} segundos")

if __name__ == "__main__":
    main()