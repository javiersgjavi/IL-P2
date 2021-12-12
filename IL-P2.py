import os
import shutil
from tkinter import *
from tkinter import messagebox
from scripts import generate_dataset, get_words_count, tf_idf_calculator, full_glossary_creator, classifier


def button_generate_dataset():
    generate_dataset.main('./data/noticias')
    messagebox.showinfo("Generate_dataset", "Dataset generated successfully")

def button_words_count():
    get_words_count.main('./data/dataset', excluded='./stop_words.txt')
    messagebox.showinfo("Generate_words_count", "Words count generated successfully")

def button_tf_idf():
    tf_idf_calculator.main('./data/outputs/word_counter/')
    messagebox.showinfo("Generate_TF-IDF", "TF-IDF calculated successfully")

def button_glossary():
    full_glossary_creator.main('./data/outputs/tf-idf/50/', excluded='./stop_words.txt')
    messagebox.showinfo("Generate_glossary", "Glossary generated successfully")

def button_classifier():
    accuracy, cat_accuracy = classifier.main('./data/dataset', glossary_path='./data/outputs/glossaries/glossary_50.txt', contador_outputs='./data/outputs/word_counter/', similarities_path = './data/outputs/ordered_by_similarity/')
    message = f'Accuracy = {accuracy}\n\nAccuracy by category:\n'
    for category in cat_accuracy.keys():
        message += f'\n\t{category} = {str(cat_accuracy[category])}'

    messagebox.showinfo("Classification accuracy", message)

def button_restart():
    respuesta = messagebox.askquestion("Restart_repository", "Are you sure you want to delete all data generated by the program?", icon='warning')
    if respuesta:
        for folder in os.listdir('./data/'):
            if folder != 'noticias':
                shutil.rmtree('./data/' + folder)

def main():

    raiz = Tk(className="IL-P2")
    raiz.geometry("500x1")
    menu = Menu(raiz)
    menu = Menu(menu, tearoff=0)

    # Generate dataset
    menu.add_command(label="1- Generate_dataset", command=button_generate_dataset)

    # Generate words count

    menu.add_command(label="2- Generate_words_count", command=button_words_count)

    # Generate TF-IDF
    menu.add_command(label="3- Generate_TF-IDF", command=button_tf_idf)

    # Generate full glossary
    menu.add_command(label="4- Generate_glossary", command=button_glossary)

    # Classify
    menu.add_command(label="5- Classify", command=button_classifier)

    # Restart configuration
    menu.add_command(label="Restart_repository", command=button_restart)

    #menu.add_cascade(label="Dataset", menu=menudatos)

    raiz.config(menu=menu)
    raiz.mainloop()


if __name__=='__main__':
    main()
