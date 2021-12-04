import os
import numpy as np

def remove_special_characters(text):
    special_characters = '!¡¿?«»“”@#$%^&*()[]{};:,./<>?\|`~-=_+"•0123456789'
    for character in special_characters:
        text = text.replace(character, '')
    return text

def read_text(path):

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

def write_output(count_words, category):

    file_path = '../data/outputs/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open(f'{file_path}test/{category}', 'a+', encoding='utf_8') as f:
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
        print('VECTOR CATEGORY: ' + str(vector_category) + ' size: '+ str(vector_category.size))
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
        print('VECTOR CATEGORY: ' + str(vector_category) + ' size: '+ str(vector_category.size))
        return vector_category
def main(path_data, excluded=None, glossary_path=None, category_glossaries=None):
    glossary = read_text(glossary_path)
    glossary_dictionary = dict()
    glossary_dictionary = get_glossary_dictionary(glossary, glossary_dictionary)

    categories = []
    category_vectors =[]
    file_vectors = []
    real_categories = []

    for category in os.listdir(path_data):
        categories.append(category)
        path_category = f'./{path_data}/{category}/test/'
        files = os.listdir(path_category)

        for file in files:
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

            print('category: '+category+' vector: ' + str(vector_file))
            write_output(res, category+'/'+file)

    #COMMENTED: CATEGORY VECTORS WITH TF-IDF

    #csvs = os.listdir(category_glossaries)
    #category_vector_dictionary = dict()
    #for category_csv in csvs:
        #category_vectors.append(get_category_vector(f'{category_glossaries}{category_csv}', glossary_dictionary))

    contador_outputs = '../data/outputs/contador/'
    txts = os.listdir(contador_outputs)
    category_vector_dictionary = dict()
    for category_txt in txts:
        category_vectors.append(get_category_vector(f'{contador_outputs}{category_txt}', glossary_dictionary))

    counter = 0
    right_guesses_counter = 0
    category_right_guesses = dict()
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
    for category in category_right_guesses:
        print(category + " accuracy: " + str(category_right_guesses[category]/(total_size/3)))



if __name__ == '__main__':
    # Get the current working directory
    main('../data/dataset', excluded='../stop_words.txt', glossary_path	 ='../data/outputs/glossary_50.txt', category_glossaries = '../data/outputs/tf-idf/50/')
