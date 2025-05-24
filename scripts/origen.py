# open catalogos.pkl
import pickle

def open_dict(file_path):
    with open(file_path, 'rb') as file:
        dic = pickle.load(file)
        return dic
    
catalogos = open_dict("../data/catalogos_generated.pkl")

# Get only origen dataframe
catalogo_origen = catalogos['ORIGEN']

print(catalogo_origen)

# Validate origen data for a row
# Should be 1, 2, 99
# If not, it is an error, show the row

def validate_origen(row):
    actual_value = row[2]
    if actual_value != "1" and actual_value != "2" and actual_value != "99":
        print(f"Error ORIGEN en registro: {row}, value: {actual_value}")
        return True

    return False
