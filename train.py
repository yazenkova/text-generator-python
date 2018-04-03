# Программа, которая считывает тексты и на их основе строит модель частот пар.
# Функция read_data() считывает из консоли: --input-dir с путем до файлов,
# --model с путем до файла, в который загружается модель,
# необязательный аргумент --lc, который включает приведение всех слов
# к нижнему регистру, на выходе отдает значения аргументов.
# Функция read_files() считывает файлы из указанного пути --input-dir построчно
# (если путь не указан, то stdin), по текстам строит модель частот пар слов
# и множество всех слов, далее сохраняет эти данные в файл с путем --model

import sys
import re
import argparse
import os
import pickle
from collections import Counter


def read_data():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', default=None, dest='dir',
                        help='path to collection of text files')
    parser.add_argument('--model', action='store', required=True, dest='m',
                        help='path to file for storage a text model')
    parser.add_argument('--lc', action='store_true', dest='lc',
                        help='make text in lower case')

    result = parser.parse_args()

    return vars(result)


# считывание одной строки и сохранение информации
def read_line(lc, line, set_words, freq_words):
    if lc:
        line = line.lower()
    words = re.findall(r'[a-zA-Zа-яА-я]+', line)
    w = set(words)
    set_words.update(w)
    list_pair = [words[i] + ' ' + words[i + 1] for i in range(len(words) - 1)]
    freq_words += Counter(list_pair)
    words.clear()


def read_files(dir, m, lc):
    # обрабатываем построчно тексты, строя множество всех слов
    # set_words и словарь частот frequency_words вида
    # {'a b':'k'}, где a, b - пара слов, k - частота
    freq_words = Counter()
    set_words = set()
    # Если директория с колекцией документов задана:
    if dir is not None:
        files = os.listdir(dir)
        os.chdir(dir)
        for doc in files:
            if doc[0] != '.' and os.path.isfile(doc):
                with open(doc) as f:
                    for line in f:
                        read_line(lc, line, set_words, freq_words)
    # Если ввод stdin
    else:
        for line in sys.stdin:
            read_line(lc, line, set_words, freq_words)

    # сохранение множества слов и множества пар слов с частотами

    data = [set_words, freq_words]

    with open(m, 'wb') as f:
        pickle.dump(data, f)


if __name__ == '__main__':
    res = read_data()
    read_files(**res)
