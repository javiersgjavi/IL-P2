import os
import pandas as pd


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
        
    data.to_csv('../data/outputs/tf-idf.csv')


def main(path):
    cargar_palabras(path)
        

if __name__ == '__main__':
    main('../data/outputs/contador/')