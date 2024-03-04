import json

# Считываем инвертированный индекс
def inverted_index(filename):
    inderted_index = {}

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Отделяем лемму и группу, убираем символ новой строки
            word, inedx_group = line.strip().split(': ')
            # Преобразуем строку с группами в список, используя json.loads
            # для корректного превращения строки формата списка в Python список
            groups_list = json.loads(inedx_group.replace('\'', '\"'))
            inderted_index[word] = groups_list

    return inderted_index

def boolean_and(set1, set2):
    return set1 & set2


def boolean_or(set1, set2):
    return set1 | set2


def boolean_not(universe_set, subset):
    return universe_set - subset


# Проверим есть ли терм в инвертированном индексе и возвращаем соответствующее множество
def get_term_set(inverted_index, term, universe_set):
    if term.startswith("NOT "):
        term = term[4:]  # Удаляем 'NOT '
        return boolean_not(universe_set, set(inverted_index.get(term, [])))
    else:
        return set(inverted_index.get(term, []))


def boolean_search(inverted_index, query):
    # Создаем общее множество всех индексов
    universe_set = set()
    for postings in inverted_index.values():
        universe_set.update(postings)

    # Сплитим запрос на отдельные операции
    operations = query.split(" AND ")
    and_results = []

    for operation in operations:
        # Разделяем элементы по OR
        or_results = set()
        or_terms = operation.split(" OR ")
        for term in or_terms:
            term_set = get_term_set(inverted_index, term, universe_set)
            or_results = boolean_or(or_results, term_set)
        # После OR объединений, мы собираем общий AND результат
        if and_results:
            # Если есть существующий AND результат, делаем логическое И с текущим набором
            and_results = boolean_and(and_results, or_results)
        else:
            # Если это первый результат - просто сохраняем его
            and_results = or_results

    return and_results

file_name = "inverted_index.txt"
index = inverted_index(file_name)
while True:
    query = input("Введите query (или -1 для выхода): ")
    if query == "-1":
        break
    print(boolean_search(index, query))