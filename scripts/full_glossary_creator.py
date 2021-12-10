import os

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

def count_words(words, count_words):
    

    for word in words:
        if word in count_words:
            count_words[word] += 1
        else:
            count_words[word] = 1

    return count_words

def delete_excluded_words(path, sorted_count_words):
    with open(path, 'r', encoding='utf_8') as f:
        excluded_words = f.read().split('\n')
        excluded_words = [word.strip() for word in excluded_words]

        for excluded in excluded_words:
            sorted_count_words.pop(excluded, None)

    return sorted_count_words

def write_output(count_words):
    sorted_count_words = dict(sorted(count_words.items(), key=lambda x: x[1], reverse=True))

    file_path = '../data/outputs/glossaries/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open(f'{file_path}glossary_50.txt', 'w', encoding='utf_8') as f:
        for word in sorted_count_words.keys():
            if not word.startswith('palabrastfidf'):
                f.write(f'{word},\n')

def main(path_data, excluded=None):
    files = os.listdir(path_data)
    res  = dict()

    for file in files:
        path_file = f'{path_data}{file}'
        words = read_text(path_file)
        res = count_words(words, res)

        if excluded:
            res = delete_excluded_words(excluded, res)
    
   
        write_output(res)

if __name__ == '__main__':
    # Get the current working directory
    main('../data/outputs/tf-idf/50/', excluded='../stop_words.txt')
