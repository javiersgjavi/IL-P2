from tkinter import *
from scripts import get_words_count, tf_idf_calculator, full_glossary_creator, classifier


def button_words_count():
    get_words_count.main('../data/dataset', excluded='../stop_words.txt')

def button_tf_idf():
    tf_idf_calculator.main('../data/outputs/contador/')

def button_glossary():
    full_glossary_creator.main('../data/outputs/tf-idf/50/', excluded='../stop_words.txt')

def classifier():
    classifier.main('../data/dataset', excluded='../stop_words.txt', glossary_path='../data/outputs/glossary_50.txt', category_glossaries='../data/outputs/tf-idf/50/')

def main():

    #generate_words_count.main('../data/dataset', excluded='../stop_words.txt')
    #tf_idf_calculator.main('../data/outputs/contador/')
    #full_glossary_creator.main('../data/outputs/tf-idf/50/', excluded='../stop_words.txt')
    #classifier.main('../data/dataset', excluded='../stop_words.txt', glossary_path='../data/outputs/glossary_50.txt', category_glossaries='../data/outputs/tf-idf/50/')

    raiz = Tk()
    menu = Menu(raiz)

   # Generate words count
    menu = Menu(menu, tearoff=0)
    menu.add_command(label="Generate_words_count", command=button_words_count)

    # Generate TF-IDF
    menu.add_command(label="Generate_TF-IDF", command=button_tf_idf)

    # Generate full glossary
    menu.add_command(label="Generate_full_glossary", command=button_glossary)

    # Classify
    menu.add_command(label="Classify", command=button_glossary) 

    #menu.add_cascade(label="Dataset", menu=menudatos)

    raiz.config(menu=menu)
    raiz.mainloop()


if __name__=='__main__':
    main()