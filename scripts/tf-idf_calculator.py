import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def cargar_palabras(path):
    data = pd.DataFrame()
    output = dict()

    # Read outputs data
    for index, f in enumerate(os.listdir(path)):
        data_file = pd.read_csv(f'{path}{f}', header=None)
        output[index] = data_file.iloc[:100]

    indice = set()
    for i in range(len(output)):
        palabras = output[i][0]
        for palabra in palabras: 
            indice.add(palabra)

    data['palabras'] = list(indice)
    data = data.set_index('palabras')
    
    for index, f in enumerate(os.listdir(path)):
        palabras_categoria = output[index].set_index(0)
        column_name = f.split('.')[0]
        column_values = []

        for palabra in data.index:
            if palabra in palabras_categoria.index:
                column_values.append(palabras_categoria.loc[palabra].values[0])

            else:
                column_values.append(0)

        data[column_name] = column_values
        
    return data

def calculate_idf(data):
    idf_values = []
    N_documentos = len(data.columns)

    for i in range(len(data)):
        count_words = np.array(data.iloc[i,:].values)
        n_documentos = (count_words>0).sum()

        value = np.log10(N_documentos/n_documentos)
        idf_values.append(value)
        
    data['idf'] = idf_values
    return data




def calculate_tf_idf(data):
    
    
    categories = data.columns[:-1]
    for category in categories:
        max_value = np.max(data[category])
        tf_idf_values =[]
        for palabra in data.index:
            count, idf = data.loc[palabra, [category, 'idf']].values
            count_norm = count/max_value
            tf_idf_values.append(count_norm* idf)

        data[f'tf-idf_{category}'] = tf_idf_values

    return data


def get_glosaries(data, path):

    path_all = f'{path}/todos/'
    path_30 = f'{path}/30/'
    if not os.path.exists(path_all):
        os.makedirs(path_all)

    if not os.path.exists(path_30):
        os.makedirs(path_30)

    for category in data.columns[-3:]:
        data_category = data[category].sort_values(ascending=False)
        
        data_category.to_csv(f'{path_all}{category}.csv')
        data_category.iloc[:30].to_csv(f'{path_30}{category}.csv')

def main(path): 
    path_output = '../data/outputs/tf-idf/'
    if not os.path.exists(path_output):
        os.makedirs(path_output)

    data = cargar_palabras(path)
    data = calculate_idf(data)
    data = calculate_tf_idf(data)
    
    data.to_csv(f'{path_output}/tf-idf.csv')

    get_glosaries(data, path_output)
        

if __name__ == '__main__':
    main('../data/outputs/contador/')