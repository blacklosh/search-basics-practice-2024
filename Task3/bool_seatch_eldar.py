from eldar import Index
import os

# Считываем html файлы которые мы сохранили в Task1
def read_html_files_to_list(dirname):
    list_html = []
    # Перебираем файлы в указанной директории
    for file in os.listdir(dirname):
        with open(dirname + "/" + file, 'r', encoding='utf-8') as f:
            list_html.append(f.read())

    return list_html

def read_html_files_to_map(dirname):
    html_map = {}
    # Перебираем файлы в указанной директории
    for file in os.listdir(dirname):
        with open(dirname + "/" + file, 'r', encoding='utf-8') as f:
            html_map[int(os.path.splitext(file)[0])] = f.read()

    return html_map

filesdir = 'c:/cfg/crawl5/pages'
documents = read_html_files_to_list(filesdir)
map = read_html_files_to_map(filesdir)

index = Index(ignore_case=True, ignore_accent=True)
index.build(documents)  # must only be done once
index.save("index.p")  # but documents are copied to disk
index = Index.load("index.p")

while True:
    query = input("Введите query (или -1 для выхода): ")
    if query == "-1":
        break
    list = index.search(query)
    matching_keys = []
    for key, value in map.items():
        # Если значение текста есть в списке
        if value in list:
            # Тогда добавляем ключ в список ключей
            matching_keys.append(key)

    matching_keys.sort()
    print(matching_keys)

