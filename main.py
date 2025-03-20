import os
import glob
from pprint import pprint

def read_cookbook(filename):
    """
    Читает файл рецептов и возвращает словарь с блюдами и их ингредиентами
    """
    cookbook = {}

    with open(filename, encoding="utf-8") as file:
        while True:
            dish_name = file.readline().strip()
            if not dish_name:
                break
            num_ingredients = int(file.readline().strip())
            ingredients = []
            for _ in range(num_ingredients):
                name, quantity, measure = file.readline().strip().split(" | ")
                ingredients.append({
                    'ingredient_name': name,
                    'quantity': int(quantity),
                    'measure': measure
                })
            cookbook[dish_name] = ingredients
            file.readline()  # Пропускаем пустую строку между блюдами

    return cookbook


def get_shop_list_by_dishes(dishes, person_count, cook_book):
    """
    Формирует список покупок для заданных блюд и количества человек
    """
    shop_list = {}

    for dish in dishes:
        if dish in cook_book:
            for ingredient in cook_book[dish]:
                ingredient_name = ingredient['ingredient_name']
                quantity = ingredient['quantity'] * person_count
                measure = ingredient['measure']

                if ingredient_name in shop_list:
                    shop_list[ingredient_name]['quantity'] += quantity
                else:
                    shop_list[ingredient_name] = {
                        'measure': measure,
                        'quantity': quantity
                    }

    return shop_list


def merge_files(file_list, output_file):
    """
    Объединяет содержимое файлов в один файл, добавляя название и количество строк
    """
    file_info = []
    for file_name in file_list:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.readlines()
            num_lines = len(content)
            file_info.append((file_name, num_lines, content))

    # Сортируем файлы по количеству строк
    file_info.sort(key=lambda x: x[1])

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_name, num_lines, content in file_info:
            # Записываем имя файла, количество строк и содержимое
            outfile.write(f"{os.path.basename(file_name)}\n{num_lines}\n")
            outfile.writelines(content)
            outfile.write("\n")


def main():
    """
    Основная функция программы. Считывает рецепты, формирует список покупок и объединяет файлы
    Функция также позволяет избежать глобальных переменных
    """
    cook_book = read_cookbook('recipes.txt')
    shopping_list = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2, cook_book)
    folder_path = './files'  # Относительный путь к папке files
    file_list = glob.glob(os.path.join(folder_path, '*.txt'))  # Получаем список всех .txt файлов
    print("Задача 1: \n")
    pprint(cook_book)
    print("Задача 2: \n")
    pprint(shopping_list)
    print("\nЗадача 3 в файле merged.txt ")
    merge_files(file_list, 'merged.txt')

main()
