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
        f = open(path)
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

        vector_category = np.array(vector_values)
        print('vector category '+path+': ' + str(vector_category))
        return vector_category

def main(path_data, excluded=None, glossary_path=None, category_glossaries=None):



    glossary = read_text(glossary_path)
    glossary_dictionary = dict()
    glossary_dictionary = get_glossary_dictionary(glossary, glossary_dictionary)


    csvs = os.listdir(category_glossaries)

    category_vector_dictionary = dict()
    for category_csv in csvs:
        category_vector_dictionary[category_csv] = get_category_vector(f'{category_glossaries}{category_csv}', glossary_dictionary)

    for category in os.listdir(path_data):
        path_category = f'./{path_data}/{category}/test/'
        files = os.listdir(path_category)

        for file in files:
            path_file = f'{path_category}{file}'
            words = read_text(path_file)
            res = glossary_dictionary.copy()
            res = count_words_glossary(words, res)
            file_values = []
            for word in res:
                file_values.append(res[word])
            vector_file = np.array(file_values)
            write_output(res, category+'/'+file)

if __name__ == '__main__':
    # Get the current working directory
    main('../data/dataset', excluded='../stop_words.txt', glossary_path	 ='../data/outputs/glossary.txt', category_glossaries = '../data/outputs/tf-idf/30/')
