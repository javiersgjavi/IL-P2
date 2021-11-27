import os

def read_text(path):

    with open(path, 'r') as f:
        text = f.read()

    words = text.split()
    words = [word.strip('.,!?:;') for word in words]
    words = [word.lower() for word in words]

    return words

def count_words_sorted(words):
    count_words = dict()
    for word in words:
        if word in count_words:
            count_words[word] += 1
        else:
            count_words[word] = 1

    sorted_count_words = dict(sorted(count_words.items(), key=lambda x: x[1], reverse=True))
    return sorted_count_words

def delete_excluded_words(path, sorted_count_words):
    with open(path, 'r') as f:
        excluded_words = f.read().split(',')
        excluded_words = [word.strip() for word in excluded_words]

        for excluded in excluded_words:
            sorted_count_words.pop(excluded, None)

    return sorted_count_words

def write_output(sorted_count_words):
    with open('output.txt', 'w') as f:
        for word in sorted_count_words.keys():
            f.write(f'{word},{sorted_count_words[word]}\n')

def main(path, excluded=None):

    words = read_text(path)
    sorted_count_words = count_words_sorted(words)

    if excluded:
        sorted_count_words = delete_excluded_words(excluded, sorted_count_words)

    write_output(sorted_count_words)
        
if __name__ == '__main__':
    # Get the current working directory
    main('./texto.txt', excluded='./excluded_words.txt')