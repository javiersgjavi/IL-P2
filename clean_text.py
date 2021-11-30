import os

def remove_special_characters(text):
    special_characters = '!¡¿?«»“”@#$%^&*()[]{};:,./<>?\|`~-=_+"•0123456789'
    for character in special_characters:
        text = text.replace(character, '')
    return text

def read_text(path):

    with open(path, 'r') as f:
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
    with open(path, 'r') as f:
        excluded_words = f.read().split('\n')
        excluded_words = [word.strip() for word in excluded_words]

        for excluded in excluded_words:
            sorted_count_words.pop(excluded, None)

    return sorted_count_words

def write_output(count_words, category):
    sorted_count_words = dict(sorted(count_words.items(), key=lambda x: x[1], reverse=True))

    if not os.path.exists('./outputs/'):
        os.makedirs('./outputs/')

    with open(f'./outputs/{category}.txt', 'w') as f:
        for word in sorted_count_words.keys():
            f.write(f'{word},{sorted_count_words[word]}\n')

def main(path_data, excluded=None):
    for category in os.listdir(path_data):
        res = dict()
        path_category = f'./{path_data}/{category}/train/'
        files = os.listdir(path_category)
        
        for file in files:
            path_file = f'{path_category}{file}'
            words = read_text(path_file)
            res = count_words(words, res)

            if excluded:
                res = delete_excluded_words(excluded, res)

            write_output(res, category)
        
if __name__ == '__main__':
    # Get the current working directory
    main('./dataset', excluded='./stop_words_2.txt')