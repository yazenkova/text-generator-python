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
import re


def read_data():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', dest='m',
                        help='path to model')
    parser.add_argument('-s', '--seed', default=None, dest='s',
                        help='first word of new text')
    parser.add_argument('-l', '--length', dest='l',
                        help='length of a new text')
    parser.add_argument('-o', '--output', default=None, dest='o',
                        help='path to output file')

    result = parser.parse_args()

    return vars(result)


def make_text(m, s, l, o):
    model = open(m, "r")

    list_words = []
    frequency_words = {}

    list_number = int(model.readline())
    for i in range(list_number):
        list_words.extend(re.findall(r'[a-zA-Z]+', model.readline()))
    frequency_number = int(model.readline())
    for i in range(frequency_number):
        list = model.readline().split()
        frequency_words[list[0] + ' ' + list[1]] = list[2]
    model.close()

    if s is not None:
        word = s
        text = [word]
    else:
        word = random.choice(list_words)
        text = [word]

    for n in range(int(l)-1):
        list = []
        for i in list_words:
            if frequency_words.get(word + ' ' + i) is not None:
                k = int(frequency_words[word + ' ' + i])
                for j in range(k):
                    list.extend(i)
        if len(list) == 0:
            list.append(random.choice(list_words))
        next_word = random.choice(list)
        text.append(next_word)
        word = next_word

    if o is not None:
        out = open(o, "w")
        out.writelines("%s " % i for i in text)
        out.close()
    else:
        for i in text:
            print(i, end=' ')


res = read_data()
make_text(**res)
