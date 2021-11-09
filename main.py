"""
    Written by Paula Yamashita de Moura - ID: 15245590 - MSWE 2023 - November 2021
    SWE 247P - Applied Information Retrieval

    This a program reads the text files produced in the previous module (text transformation)
    and produces an inverted index.

"""
import glob
import os
import re
from collections import defaultdict
from typing import List, Dict


class InvertedIndex:
    def __init__(self):
        self.dictionary: Dict[str, List[WordInDocument]] = {}
        self.dump_to_disk = 0
        self.tokens_qty = 0

    def process_text(self, text_file, _file_count):
        if self.tokens_qty < 1000000:
            words_to_add = text_tokenizer(text_file)
            for i, word in enumerate(words_to_add):
                if word not in self.dictionary or not self.dictionary[word]:
                    wid = WordInDocument(_file_count)
                    self.dictionary[word] = [wid]
                elif self.dictionary[word][-1].doc_number != _file_count:
                    wid = WordInDocument(_file_count)
                    self.dictionary[word].append(wid)
                else:
                    wid = self.dictionary[word][-1]
                wid.insert_to_list(i)
                self.tokens_qty += 1
        else:
            print('limit reached')
            self.write_partial_index()
            self.dump_to_disk += 1
            self.tokens_qty = 0

    def write_partial_index(self):
        str_to_file = ''
        cur_letter = ''
        fp = None
        for word in sorted(self.dictionary):
            if self.dictionary[word]:
                if word[0] != cur_letter:
                    if str_to_file != '':
                        fp = open(
                            os.path.join('SWE247P project', 'inv-index', 'temp_files',
                                         cur_letter + "-" + str(self.dump_to_disk) +
                                         '.txt'), 'w')
                        fp.write(str_to_file)
                        fp.close()
                    cur_letter = word[0]
                    str_to_file = ''
                elements_str = ''
                for elem in self.dictionary[word]:
                    positions_str = ','.join(str(x) for x in elem.appearance)
                    elements_str = elements_str + f'{elem.doc_number}:{len(elem.appearance)}:{positions_str};'
                str_to_file = str_to_file + f'{word} {elements_str}\n'
                self.dictionary[word] = []

    def size_of_dict(self):
        total_words = len(self.dictionary)
        total_positions = 0
        for w in self.dictionary:
            for p in self.dictionary[w]:
                total_positions = total_positions + len(p.appearance)
        total_size = total_words + total_positions
        return total_size

    def print_dict(self):
        for word in sorted(self.dictionary):
            print(f'{word} ', end="", flush=True)
            for elem in self.dictionary[word]:
                print(f'{elem.doc_number}:{len(elem.appearance)}:', end="", flush=True)
                positions = elem.appearance
                print(*positions, sep=',', end=';')
            print('')

    def merge_inverted_index(self):
        self.dictionary = defaultdict(str)
        for i in [chr(x) for x in list(range(48, 58)) + list(range(97, 127))]:
            for idx_file in glob.glob(f'SWE247P project/inv-index/temp_files/**/{i}*.txt', recursive=True):
                with open(idx_file) as curr_file:
                    for line in curr_file:
                        tokens = line.strip().split(' ')
                        tk = tokens[0]
                        tk_info = tokens[1]
                        self.dictionary[tk] += tk_info
            self.write_index_file()
            self.dictionary = defaultdict(str)
            # print(self.dictionary)

    def write_index_file(self):
        line_to_index = ''
        cur_letter = '0'
        fp = None
        for token in sorted(self.dictionary):
            if self.dictionary[token]:
                if token[0] == cur_letter and line_to_index != '':
                    # if cur_letter:
                    fp = open(
                        os.path.join('SWE247P project', 'inv-index',
                                     token[0] + '.txt'), 'a')
                    fp.writelines(line_to_index)
                    fp.close()
                    line_to_index = ''
                cur_letter = token[0]
                line_to_index = (token + " " + str(self.dictionary[token] + '\n'))

            print(line_to_index)



            # elements = ''.join(str(x) for x in self.dictionary[word])
            # line_to_index = word + ' ' + elements

            # for elem in self.dictionary[word]:

            #     position = ''.join(str(x) for x in elem.appearance)
            #     element = element + f'{elem.doc_number}:{len(elem.appearance)}:{position};'
            # end_line = end_line + f'{word} {element}\n'


class WordInDocument:
    def __init__(self, _doc_number):
        self.doc_number = _doc_number
        self.appearance = []

    def insert_to_list(self, position):
        self.appearance.append(position)


def text_tokenizer(text_to_tokenize):
    tokens_list = text_to_tokenize.read().split()
    return tokens_list


if __name__ == '__main__':
    my_path = 'C:\\Users\\paula\\PycharmProjects\\InvertedIndex\\SWE247P project\\input-transform\\'
    files = []
    file_count = 0
    index = InvertedIndex()
    for filename in glob.glob('SWE247P project/input-transform/**/*.txt', recursive=True):
        file_number = filename[-9:-4]
        files.append({'file_number': file_number, 'file_path': filename})
        with open(os.path.join(os.getcwd(), filename), 'r') as myfile:
            index.process_text(myfile, file_count)
        file_count += 1
    # index.print_dict()
    # print(files)
    # index.write_index_file()
    InvertedIndex().merge_inverted_index()
