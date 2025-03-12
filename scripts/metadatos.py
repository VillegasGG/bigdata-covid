import pandas as pd

def open_metadata_file(file_path):
    '''
    Open a metadata  xlsx file where:
        - first row: metadata number
        - second row: metadata names
        - third row: metadata description'
        - fourth row: metadata format
    '''
    local_metadata_types = {}
    formats_dicc = {'TEXTO': 'str', 'AAAA-MM-DD': 'datetime64[ns]'}
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
        
metadata_types = open_metadata_file("../data/metadatos_descriptores.xlsx")

print(metadata_types)