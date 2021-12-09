from scripts import generate_words_count, tf_idf_calculator, full_glossary_creator, classifier

def main():

    generate_words_count.main('../data/dataset', excluded='../stop_words.txt')
    tf_idf_calculator.main('../data/outputs/contador/')
    full_glossary_creator.main('../data/outputs/tf-idf/50/', excluded='../stop_words.txt')
    classifier.main('../data/dataset', excluded='../stop_words.txt', glossary_path='../data/outputs/glossary_50.txt', category_glossaries='../data/outputs/tf-idf/50/')

if __name__=='__main__':
    main()