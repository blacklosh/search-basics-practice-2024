import json
import os

# Считываем файл леммы, который мы создали в Task2
def read_lemmas_file(filename):
    lemmas = {}

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Отделяем лемму и группу, убираем символ новой строки
            lemma, groups_str = line.strip().split(': ')
            # Преобразуем строку с группами в список, используя json.loads
            # для корректного превращения строки формата списка в Python список
            groups_list = json.loads(groups_str.replace('\'', '\"'))
            lemmas[lemma] = groups_list

    return lemmas

# Считываем html файлы которые мы сохранили в Task1
def read_html_files_to_map(dirname):
    html_map = {}
    # Перебираем файлы в указанной директории
    for file in os.listdir(dirname):
        with open(dirname + "/" + file, 'r', encoding='utf-8') as f:
            html_map[os.path.splitext(file)[0]] = f.read()

    return html_map

# Создаем инвертированный индекс
def make_inverted_index(lemma_map, html_docs):
    result_map = {}
    for key1, words_list in lemma_map.items():
        # Создаем пустой список для сбора ключей из html_docs для текущего lemma_map.key
        matched_keys_from_html_docs = []
        for key2, text in html_docs.items():
            # Проверяем каждое слово из списка words_list
            if any(word in text for word in words_list):
                # Если слово найдено, добавляем ключ html_docs.key в список совпадений
                matched_keys_from_html_docs.append(int(key2))
        # Если были найдены совпадения, сохраняем список html_docs.key под ключом lemma_map.key
        if matched_keys_from_html_docs:
            matched_keys_from_html_docs.sort()
            result_map[key1] = matched_keys_from_html_docs
    return result_map


lemma_file = "../Task2/lemmas.txt"
filesdir = 'c:/cfg/crawl5/pages'
cfgdir = 'c:/cfg/crawl5/'

html_content_map = read_html_files_to_map(filesdir)
lemma_map = read_lemmas_file(lemma_file)
inverted_index = make_inverted_index(lemma_map, html_content_map)


# Вывод инвертированного индекса:
f = open(cfgdir+"inverted_index.txt", 'w', encoding='utf-8')
for word, group in inverted_index.items():
    s = f"{word}: {group}\n"
    print(s)
    f.write(s)
f.close()
