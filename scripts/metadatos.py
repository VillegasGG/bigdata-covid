import pandas as pd

catalogos = {}

def open_catalog_file(file_path):
    '''
    Open a catalog xlsx file where:
        - sheet name: catalog name
    '''
    catalog_dfs = {}

    try:
        catalog = pd.read_excel(file_path, sheet_name=None)
    except:
        print("Error al abrir el archivo de catalogos")
    
    if catalog is not None:
        print(catalog.keys())
        for key in catalog.keys():
            print(key)
            df_catalog = catalog[key]
            catalog_name = key.split(" ")[-1]
            catalog_dfs[catalog_name] = df_catalog

    print(catalog_dfs.keys())

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
            description = str(metadata.iloc[i, 2]).strip()
            format = str(metadata.iloc[i, 3]).strip()
            local_metadata_types[position] = {"name": name, "description": description, "format": format}

    return local_metadata_types
        

open_catalog_file("../data/catalogos.xlsx")
# metadata_types = open_metadata_file("../data/metadatos_descriptores.xlsx")