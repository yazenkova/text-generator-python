# Программа, которая на основе модели частот пар генерирует новый текст.
# На каждом шаге выбирается слово исходя из того, какое слово было предыдущим.
# Для <слово1> берутся частоты соответствующих <слов2>,
# на их основе составляется массив [<слово2-1>,
# повторённое <частота слова2-1> раз, <слово2-2>,
# повторённое <частота слова2-2-> раз, ...].
# Выбор слова из этого массива производится с помощью random.choice.
# Функция read_data() считывает из консоли: --output с путем до файла вывода
# (если не задан, то stdout), --model с путем до файла,
# в котором хранится модель, необязательный аргумент --seed - первое слово
# нового текста (если нет, то рандомное), --length - длина нового текста.
# На выходе функция отдает значения аргументов.
# Функция make_text() считывает модель из указанного пути --model,
# далее строит новый текст по алгоритму: для слова A смотрит частоты всех пар
# слов, где есть А, затем с учетом частот из них выбирает рандомное,
# и так далее. Полученный текст записывается в --output или
# выводится в stdout.

import argparse
import random
import pickle


def read_data():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', dest='model',
                        help='path to model')
    parser.add_argument('-s', '--seed', default=None, dest='seed',
                        help='first word of new text')
    parser.add_argument('-l', '--length', dest='length',
                        help='length of a new text')
    parser.add_argument('-o', '--output', default=None, dest='output',
                        help='path to output file')

    result = parser.parse_args()

    return vars(result)


# Генерируем новое слово в тексте
def choose_next_word(word, l_words, fr_words):
    frequency_list = []
    for i in l_words:
        if fr_words.get(word + ' ' + i):
            k = int(fr_words[word + ' ' + i])
            for j in range(k):
                frequency_list.append(i)
    if not frequency_list:
        frequency_list.append(random.choice(l_words))
    next_word = random.choice(frequency_list)
    return next_word


# Вывод полученного текста
def write_output(output, text):
    # Проверяем, есть ли файл output и выводим наш текст
    if output:
        out = open(output, "w")
        out.writelines("%s " % i for i in text)
        out.close()
    else:
        for i in text:
            print(i, end=' ')


# Создание текста на основе модели
def make_text(model, seed, length, output):

    # Считываем модель, составляем список слов list_words,
    # словарь частот frequency_words

    with open(model, 'rb') as f:
        data = pickle.load(f)

    list_words = [i for i in data[0]]
    frequency_words = data[1]

    # Проверяем, задано ли первое слово в аргументах
    if seed:
        word = seed
    else:
        word = random.choice(list_words)
    text = [word]

    # Для слова строим список парных ему слов с учетом частоты, из них
    # выбираем рандомом следующее слово, проделываем то же для нового и тд

    for n in range(int(length) - 1):
        next_word = choose_next_word(word, list_words, frequency_words)
        text.append(next_word)
        word = next_word

    write_output(output, text)


if __name__ == "__main__":
    res = read_data()
    make_text(**res)
