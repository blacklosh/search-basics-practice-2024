from bs4 import BeautifulSoup
import os
import math


def read_lemmas_file(filename):
    lemmas = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Отделяем лемму и группу, убираем символ новой строки
            lemma, groups_str = line.strip().split(': ')
            # Преобразуем строку с группами в список, используя json.loads
            # для корректного превращения строки формата списка в Python список
            lemmas.append(lemma)

    return lemmas

def read_tokens_file(filename):
    tokens = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            token = line.strip().split("\n")[0]
            tokens.append(token)

    return tokens


def read_html_files_to_list(dirname):
    list_html = []
    # Перебираем файлы в указанной директории
    for file in os.listdir(dirname):
        with open(dirname + "/" + file, 'r', encoding='utf-8') as f:
            list_html.append(f.read())

    return list_html
def remove_html_tags(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text()

def get_without_html_tags(html_pages):
    # Map for storing the index and corresponding cleaned text
    text_without_html_tags = []

    # Loop through the HTML pages array and populate the map
    for index, html_content in enumerate(html_pages):
        text_without_html_tags.append(remove_html_tags(html_content))

    return text_without_html_tags

def compute_tf(word, document):
    # Count the number of times the word appears in the document
    word_count = document.count(word)
    # Calculate the total number of words in the document
    total_words = len(document.split())
    # Compute the Term Frequency for the word
    tf = word_count / total_words
    return tf

def compute_idf(word, corpus):
    # Count the number of documents containing the word
    containing_docs = sum(1 for document in corpus if word in document)
    # Calculate the total number of documents
    number_of_documents = len(corpus)
    # Add 1 to the number of containing documents to prevent division by zero
    containing_docs += 1
    # Compute the Inverse Document Frequency for the word
    idf = math.log(number_of_documents / containing_docs)
    return idf

def compute_tf_idf(word, document, corpus):
    # Compute the TF for the word in the document
    tf = compute_tf(word, document)
    # Compute the IDF for the word in the corpus
    idf = compute_idf(word, corpus)
    # Calculate TF-IDF
    tf_idf = tf * idf
    return tf_idf


# Путь, где будут сохранять TF-IDF
cfgdir = 'c:/cfg/crawl5/tf-idf/'

# Путь до html страничек
filesdir = 'c:/cfg/crawl5/pages'

# Файл с леммами
lemma_file = "../Task2/lemmas.txt"

# Файл с токенам
tokens_file = "../Task2/tokens.txt"


lemmas = read_lemmas_file(lemma_file)
tokens = read_tokens_file(tokens_file)
html_pages = get_without_html_tags(read_html_files_to_list(filesdir))

for index, html_content in enumerate(html_pages):
    file_name_token = f"{index}_tokens.txt"
    file_name_lemma = f"{index}_lemmas.txt"

    f = open(cfgdir + file_name_token, 'w', encoding='utf-8')
    for token in tokens:
        tf = compute_tf(token, html_content)
        tf_idf = compute_tf_idf(token, html_content, html_pages)
        s = f"{token} {tf} {tf_idf}\n"
        print(s)
        f.write(s)
    f.close()

    f = open(cfgdir + file_name_lemma, 'w', encoding='utf-8')
    for lemma in lemmas:
        tf = compute_tf(lemma, html_content)
        tf_idf = compute_tf_idf(lemma, html_content, html_pages)
        s = f"{lemma} {tf} {tf_idf}\n"
        print(s)
        f.write(s)
    f.close()
