import re
from collections import defaultdict
import numpy as np

# Считывание и парсинг файла обратного индекса
def read_inverted_index(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        inverted_index = {}
        for line in f:
            word, pages = line.strip().split(': ')
            pages = pages.replace('[', '').replace(']', '').replace(' ', '').split(',')
            inverted_index[word] = [int(page) for page in pages]
    return inverted_index

# Расчет вектора запроса
def get_query_vector(query, inverted_index):
    query_words = query.lower().split()
    query_vector = defaultdict(int)
    for word in query_words:
        if word in inverted_index:
            query_vector[word] += 1
    return query_vector

# Расчет вектора документа
def get_document_vector(doc_id, inverted_index):
    doc_vector = defaultdict(int)
    for word, pages in inverted_index.items():
        if doc_id in pages:
            doc_vector[word] += 1
    return doc_vector

# Расчет схожести (косинусная метрика)
def cosine_similarity(vector1, vector2):
    # Найти общие ключи для обоих векторов
    keys = set(vector1.keys()).union(set(vector2.keys()))
    v1 = np.array([vector1.get(k, 0) for k in keys])
    v2 = np.array([vector2.get(k, 0) for k in keys])

    dot_product = np.dot(v1, v2)
    norm_vector1 = np.linalg.norm(v1)
    norm_vector2 = np.linalg.norm(v2)

    return dot_product / (norm_vector1 * norm_vector2) if norm_vector1 * norm_vector2 != 0 else 0

# Векторный поиск
def vector_search(query, inverted_index):
    query_vector = get_query_vector(query, inverted_index)
    scores = {}
    for doc_id in set(page for pages in inverted_index.values() for page in pages):
        doc_vector = get_document_vector(doc_id, inverted_index)
        score = cosine_similarity(query_vector, doc_vector)
        if score > 0:
            scores[doc_id] = score
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)

def load_file_names(index_file_name):
    with open(index_file_name, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        index_to_links = {}
        for line in lines:
            arr = line.split(' ')
            arr[0] = arr[0].replace('c:/cfg/crawl5/', '').replace('.html', '')
            index_to_links[int(arr[0])] = arr[1].replace('\n', '')
        return index_to_links

