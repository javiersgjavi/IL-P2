import os
import pandas as pd
import numpy as np

def remove_special_characters(text):
    special_characters = '!¡¿?«»“”@#$%^&*()[]{};:,./<>?\|`~-=_+"•0123456789'
    for character in special_characters:
        text = text.replace(character, '')
    return text

def read_text(path):
    #print('Path: '+ path)
    with open(path, 'r', encoding='utf_8') as f:
        text = f.read()

    text_clean = remove_special_characters(text)
    words = text_clean.split()
    words = [word.strip('.,!?:;') for word in words]
    words = [word.lower() for word in words]

    return words

def count_words_glossary(words, count_words):
    for word in words:
        if word in count_words:
            count_words[word] += 1
    return count_words

def get_glossary_dictionary(words, count_words):
    for word in words:
        if word in count_words:
            count_words[word] += 1
        else:
            count_words[word] = 0

    return count_words

def delete_excluded_words(path, sorted_count_words):
    with open(path, 'r', encoding='utf_8') as f:
        excluded_words = f.read().split('\n')
        excluded_words = [word.strip() for word in excluded_words]

        for excluded in excluded_words:
            sorted_count_words.pop(excluded, None)

    return sorted_count_words

def write_output(count_words, category, file_name):

    file_path = './data/outputs/test/'
    if not os.path.exists(file_path+category):
        os.makedirs(file_path+category)

    with open(f'{file_path}{category}{file_name}', 'a+', encoding='utf_8') as f:
        for word in count_words.keys():
            f.write(f'{word},{count_words[word]}\n')

def get_category_vector(path, glossary):
        d = dict()
        f = open(path, encoding='utf_8')
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(",")
            d[key] = val
        vector_values = []
        for word in glossary:
            if word in d:
                vector_values.append(d[word])
            else:
                vector_values.append(0)

        vector_category = np.array(vector_values, dtype=float)
        max_value = np.amax(vector_category)
        contador = 0
        for value in vector_category:
            vector_category[contador] = value/max_value
            contador += 1
        #print('VECTOR CATEGORY: ' + str(vector_category) + ' size: '+ str(vector_category.size))
        return vector_category

def get_category_count_vector(path, glossary):
        words = read_text(path)
        d = glossary.copy()
        d = count_words_glossary(words, d)
        vector_values = []
        for word in glossary:
            if word in d:
                vector_values.append(d[word])
            else:
                vector_values.append(0)

        vector_category = np.array(vector_values, dtype=float)
        #print('VECTOR CATEGORY: ' + str(vector_category) + ' size: '+ str(vector_category.size))
        return vector_category

def main(path_data, glossary_path=None, contador_outputs=None, similarities_path = None):
    glossary = read_text(glossary_path)
    glossary_dictionary = dict()
    glossary_dictionary = get_glossary_dictionary(glossary, glossary_dictionary)

    categories = []
    category_vectors =[]
    file_vectors = []
    real_categories = []


    accuracy_table = pd.DataFrame()
    file_index = []
    similarity_list = []

    

    for category in os.listdir(path_data):
        categories.append(category)
        path_category = f'./{path_data}/{category}/test/'
        files = os.listdir(path_category)
        if not os.path.exists(f'{similarities_path}/{category}'):
            os.makedirs(f'{similarities_path}/{category}')
        

        for file in files:
            file_index.append(category + file)
            real_categories.append(category)
            path_file = f'{path_category}{file}'
            words = read_text(path_file)
            res = glossary_dictionary.copy()
            res = count_words_glossary(words, res)
            file_values = []
            for word in res:
                file_values.append(res[word])
            vector_file = np.array(file_values, dtype=float)
            file_vectors.append(vector_file)



            with open(f'{path_category}{file}', 'r', encoding='utf_8') as originalFile, open(f'{similarities_path}{category}{file}', 'a', encoding='utf_8') as copiedFile:
                for line in originalFile:
                    copiedFile.write(line)

            #print('category: '+category+' vector: ' + str(vector_file))
            write_output(res, category, file)
        print('Document length: ' + str(len(file_index)))
    accuracy_table['Documentos'] = list(file_index)
    print('Final Document length: ' + str(len(file_index)))
    accuracy_table = accuracy_table.set_index('Documentos')

    txts = os.listdir(contador_outputs)
    for category_txt in txts:
        category_vectors.append(get_category_vector(f'{contador_outputs}{category_txt}', glossary_dictionary))

    counter = 0
    right_guesses_counter = 0
    category_right_guesses = dict()
    predicted_categories = []
    for vector in file_vectors:
        category_counter = 0
        max_value = 0
        predicted_category = ''
        for category_vector in category_vectors:
            product = np.dot(vector, category_vector)
            similarity = product / (np.linalg.norm(vector)*np.linalg.norm(category_vector))
            if similarity >= max_value:
                max_value = similarity
                predicted_category = categories[category_counter]

            #print('file'+str(counter)+ ' '+ str(categories[category_counter])+ ': ' + str(similarity))

            category_counter += 1
        predicted_categories.append(predicted_category)
        similarity_list.append(max_value)


        copiedFile_path = similarities_path + file_index[counter]
        new_name =str(similarities_path) +str('/') + str(predicted_category) +str('/')  + str('similaridad') + str(' - ') + str(max_value*100) + str(' - ') + str(file_index[counter])
        os.rename(copiedFile_path, new_name)


        real_category = real_categories[counter]
        print('file'+str(counter)+ ' predicted_category: '+ predicted_category + ' real_category: ' + real_category)
        if predicted_category == real_category:
            right_guesses_counter += 1
            if real_category in category_right_guesses:
                category_right_guesses[real_category] += 1
            else:
                category_right_guesses[real_category] = 1
        counter += 1
    total_size = len(file_vectors)
    accuracy = right_guesses_counter / total_size
    print('overall accuracy: ' + str(accuracy))
    accuracy_category = dict()
    for category in category_right_guesses:
        accuracy_table['Predicción'] = list(predicted_categories)
        accuracy_table['Similitud'] = list(similarity_list)
        accuracy_cat = category_right_guesses[category]/(total_size/3)
        accuracy_category[category] = accuracy_cat
        print(category + " accuracy: " + str(accuracy_cat))
    #accuracy_table = data[category].sort_values(ascending=False)

    accuracy_table.to_csv(f'./data/outputs/similarity.csv')
    #accuracy_table.iloc[:100].to_csv(f'{path_100}{category}.csv')
    return accuracy, accuracy_category



if __name__ == '__main__':
    # Get the current working directory
    _ = main('./data/dataset', glossary_path	 ='./data/outputs/glossaries/glossary_50.txt', contador_outputs = './data/outputs/word_counter/', similarities_path = './data/outputs/ordered_by_similarity/')
