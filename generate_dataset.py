import os
import shutil

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def main(input_path):
    output_path = './dataset/'
    create_folder(output_path)

    categories = os.listdir(input_path)
    for category in categories:
        category_path = f'{input_path}/{category}/'
        output_category_path = f'{output_path}/{category}/'

        train_path = f'{output_category_path}/train/'
        test_path = f'{output_category_path}/test/'
        create_folder(train_path)
        create_folder(test_path)

        for f in os.listdir(category_path):
            number_file = int(f.split('.')[0])
            if number_file % 2 == 0:
                shutil.copy(f'{category_path}{f}', f'{train_path}{f}')
            else:
                shutil.copy(f'{category_path}{f}', f'{test_path}{f}')




if __name__=='__main__':
    main('./noticias')