import pandas as pd
import pickle

catalogos = {}

def open_catalog_file(file_path):
    '''
    Open a catalog xlsx file where:
        - sheet name: catalog name
    '''
    catalog_dfs = {}

    try:
        catalog = pd.read_excel(file_path, sheet_name=None)
    except Exception as e:
        print(f"Error al abrir el archivo de catalogos: {e}")
    
    if catalog is not None:
        print(catalog.keys())
        for key in catalog.keys():
            print(key)
            df_catalog = catalog[key]
            catalog_name = key.split(" ")[-1]
            catalog_dfs[catalog_name] = df_catalog

    return catalog_dfs

def open_metadata_file(file_path):
    '''
    Open a metadata  xlsx file where:
        - first row: metadata number
        - second row: metadata names
        - third row: metadata description'
        - fourth row: metadata format
    '''
    local_metadata_types = {}
    try:
        metadata = pd.read_excel(file_path)
    except:
        print("Error al abrir el archivo de metadatos")
    
    if metadata is not None:
        for i in range(len(metadata)):
            position = int(metadata.iloc[i, 0])
            name = str(metadata.iloc[i, 1]).strip()
            # description = str(metadata.iloc[i, 2]).strip()
            format = str(metadata.iloc[i, 3]).strip()
            local_metadata_types[position] = {"name": name, "format": format}

    return local_metadata_types

def clean_df(df):
    '''
    Clean a dataframe by:
        - Drop NaN values (rows)
        - Drop duplicates
    '''
    df = df.dropna()
    df = df.drop_duplicates()

    return df        

def save_dict(dic, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(dic, file)
        print("Catalogos guardados")

def save_as_csv(dic, file_path):
    '''
    Save a dictionary of dataframes as csv file with multiple sheets
        - key: sheet name
        - value: dataframe to save in a new sheet
    '''

    with pd.ExcelWriter(file_path) as writer:
        for key in dic.keys():
            dic[key].to_excel(writer, sheet_name=key)

def load_dict(file_path):
    with open(file_path, 'rb') as file:
        dic = pickle.load(file)
        return dic
    
def show_df_dic(dic):
    for key in dic.keys():
        print(key)
        print(dic[key].head())

def convert_df_to_dict(df):
    """
    Convert a dataframe to a dictionary ignoring the index
    """
    return df.to_dict(orient="records")    

def get_type(element):
    """
    Get the type of the element based on its content.
    """
    if isinstance(element, list):
        # Retorna el tipo de dato de la key 'CLAVE' del primer elemento
        return type(element[0]['CLAVE'])
    else:
        if 'TEXTO' in element:
            return str
        elif 'AAAA-MM-DD' in element:
            return pd.Timestamp
        return None

def get_metadata_types(metadata, catalogs):
    result = {}
    catalog = None

    for key in metadata.keys():
        format = metadata[key]["format"]
        # Si contiene 'CATÁLOGO', se busca en los catálogos
        if "CATÁLOGO" in format:
            if "SI_ NO" in format:
                catalog_name = "SI_NO"
            else:
                catalog_name = format.split(" ")[-1]

            try:
                catalog = convert_df_to_dict(catalogs[catalog_name])
            except:
                print(f"Error al buscar el catalogo: {catalog_name}")
        
        name = metadata[key]["name"]
        type = get_type(catalog) if catalog else get_type(format)
        result[key] = {"name": name, "type": type}

    return result

def main():
    # OPEN FILES
    catalogs = open_catalog_file("../data/catalogos.xlsx")
    metadata_types = open_metadata_file("../data/metadatos_descriptores.xlsx")

    # CLEAN CATALOGS
    for key in catalogs.keys():
        catalogs[key] = clean_df(catalogs[key])

    # PRINT CATALOGS
    # show_df_dic(catalogs)

    # PRINT METADATA
    # for key in metadata_types.keys():
    #     print(key)
    #     print(metadata_types[key])

    # SAVE CATALOGS
    save_dict(catalogs, "../data/catalogos_generated.pkl")
    save_as_csv(catalogs, "../data/catalog_generated.xlsx")

    # LOAD CATALOGS
    catalogs_open = load_dict("../data/catalogos_generated.pkl")

    # GET METADATA TYPES
    result = get_metadata_types(metadata_types, catalogs_open)

    # PRINT METADATA TYPES
    for key in result.keys():
        print(key)
        print(result[key])

    # SAVE METADATA TYPES 
    save_dict(result, "../data/metadata_types.pkl")
    
main()
