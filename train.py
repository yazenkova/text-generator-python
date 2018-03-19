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


def read_files(dir, m, lc):
    freq_words = {}
    set_words = set()

    if dir is not None:
        files = os.listdir(dir)
        for doc in files:
            if doc[0] != '.' and os.path.isfile(dir + doc):
                path = dir + doc
                with open(path) as f:
                    for line in f:
                        if lc:
                            line = line.lower()
                        words = re.findall(r'[a-zA-Z]+', line)
                        w = set(words)
                        set_words.update(w)
                        for i in range(len(words) - 1):
                            if freq_words.get(words[i] + ' ' + words[i + 1]) \
                                    is not None:
                                freq_words[words[i] + ' ' + words[i + 1]] += 1
                            else:
                                freq_words[words[i] + ' ' + words[i + 1]] = 1
                        words.clear()
    else:
        for line in sys.stdin:
            if lc:
                line = line.lower()
            words = re.findall(r'[a-zA-Z]+', line)
            print(words)
            w = set(words)
            set_words.update(w)
            print(set_words)
            for i in range(len(words) - 1):
                if freq_words.get(words[i] + ' ' + words[i + 1]) is not None:
                    freq_words[words[i] + ' ' + words[i + 1]] += 1
                else:
                    freq_words[words[i] + ' ' + words[i + 1]] = 1
            words.clear()

    out = open(m, "w")

# сохранение множества слов ( + их количество) и множества пар слов с частотами

    out.writelines("%s\n" % len(set_words))
    out.writelines("%s\n" % i for i in set_words)
    out.writelines("%s\n" % len(freq_words.keys()))
    for key in freq_words:
        out.writelines("%s %s\n" % (key, freq_words[key]))

    out.close()


res = read_data()
print(res)
read_files(**res)
