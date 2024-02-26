import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Устанавливаем необходимые компоненты NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Инициализируем лемматизатор
lemmatizer = WordNetLemmatizer()

# Загружаем список стоп-слов для английского языка
stop_words = set(stopwords.words('english'))


def tokenize_english(dirname):
    # Чтение файла
    text = ""
    for file in os.listdir(dirname):
        with open(dirname + "/" + file, 'r', encoding='utf-8') as f:
            text = text + f.read()

    # Токенизация текста
    tokens = word_tokenize(text)

    # Удаление стоп-слов, дубликатов, чисел и "мусора"
    tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
    unique_tokens = list(set(tokens))  # Убираем дубликаты

    return unique_tokens


# Функция для группировки токенов по леммам
def group_by_lemmas(tokens):
    # Создаем словарь для группировки слов по леммам
    lemmas_dict = {}
    for word in tokens:
        lemma1 = lemmatizer.lemmatize(word)
        # Добавляем слово в список его леммы
        if lemma1 in lemmas_dict:
            if word not in lemmas_dict[lemma1]:  # Убедитесь, что одинаковые слова не добавляются
                lemmas_dict[lemma1].append(word)
        else:
            lemmas_dict[lemma1] = [word]

    return lemmas_dict


def save_file(file, content):
    print(file)
    f1 = open(file, 'w', encoding="utf-8")  # открытие в режиме записи
    print(content)
    f1.write(content)
    f1.close()


# Использование функции
cfgdir = 'c:/cfg/crawl5/'
filesdir = 'c:/cfg/crawl5/pages'
unique_tokens = tokenize_english(filesdir)
lemmas_grouped = group_by_lemmas(unique_tokens)

# Сохранение всех токенов
save_file(cfgdir+"tokens.txt", ' \n'.join(unique_tokens))

sorted_lemmas_grouped = sorted(lemmas_grouped.items(), key=lambda item: len(item[1]), reverse=True)

# Вывод отсортированных групп лемм:
f = open(cfgdir+"lemmas.txt", 'w', encoding='utf-8')
for lemma, group in sorted_lemmas_grouped:
    s = f"{lemma}: {group}\n"
    print(s)
    f.write(s)
f.close()