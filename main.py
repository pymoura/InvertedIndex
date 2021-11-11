"""
    Written by Paula Yamashita de Moura - ID: 15245590 - MSWE 2023 - November 2021
    SWE 247P - Applied Information Retrieval

    This a program reads the text files produced in the previous module (text transformation)
    and produces an inverted index.

"""
import glob
import os
from collections import defaultdict
from typing import List, Dict


class InvertedIndex:
    def __init__(self):
        self.dictionary: Dict[str, List[WordInDocument]] = {}
        self.dump_to_disk = 0
        self.tokens_qty = 0

    def process_text(self, text_file, _file_count):
        """
        This methods process a text file, adds tokens to a dictionary, and when total of tokens on dictionary reaches
        1000000, call a function to write data on disk.
        :param text_file: file pointer
        :param _file_count: int

        """

        if self.tokens_qty < 10000000:
            words_to_add = text_tokenizer(text_file)
            for i, word in enumerate(words_to_add):
                #    if token(word) is not in dictionary or there is no data to this token, add token to dictionary,
                #    initialize WordInDocument object, and document number to it.
                if word not in self.dictionary or not self.dictionary[word]:
                    wid = WordInDocument(_file_count)
                    self.dictionary[word] = [wid]
                #    if token exists, check if document number is the last instance of wid doc_number. If does not exist
                #    initialize object and append it to end of list.
                elif self.dictionary[word][-1].doc_number != _file_count:
                    wid = WordInDocument(_file_count)
                    self.dictionary[word].append(wid)
                #   set wid to be the last element of list for the token
                else:
                    wid = self.dictionary[word][-1]
                #   call method to insert the positions of tokens in the text to dictionary
                wid.insert_to_list(i)
                self.tokens_qty += 1
        else:
            #  when limit (total number of tokens in dictionary) is reached, calls method to write partial index
            #  to disc, increment dumb_to_disk counter by one, reset tokens_qty counter.
            print('limit reached')
            self.write_partial_index()
            self.dump_to_disk += 1
            self.tokens_qty = 0

    def write_partial_index(self):
        """
        This method access dictionary, sort it alphabetically. and for each token(word), creates a string containing
        the word, document numbers,  and the positions  the token where found on the text. Then, creates a text file
        for each alphanumeric character and round of dumping words to disk, and writes the strings to file based on the
        first letter of token(word).
        """
        str_to_file = ''
        cur_letter = ''
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
        else:
            # z is the last letter
            fp = open(
                os.path.join('SWE247P project', 'inv-index', 'temp_files',
                             'z' + "-" + str(self.dump_to_disk) +
                             '.txt'), 'w')
            fp.write(str_to_file)
            fp.close()

    def merge_inverted_index(self):
        """
        This method gets the text files containing partial index and merges them in a final index. For each alphanumeric
        character, tokenizes the text by line and splits tokens between word and word's location/positions. Add the
        tokens to a new dictionary. Then call method to write a final index.

        """
        self.dictionary = defaultdict(str)
        for i in [chr(x) for x in list(range(48, 58)) + list(range(97, 123))]:
            for idx_file in glob.glob(f'SWE247P project/inv-index/temp_files/**/{i}*.txt', recursive=True):
                with open(idx_file) as curr_file:
                    for line in curr_file:
                        tokens = line.strip().split(' ')
                        tk = tokens[0]
                        tk_info = tokens[1]
                        self.dictionary[tk] += tk_info
                os.remove(idx_file)
            self.write_merged_index_file(i)
            self.dictionary = defaultdict(str)

    def write_merged_index_file(self, cur_letter):
        """
        This method receives a dictionary with a single first character ('a' or 'b' or 'c' ..), sorts it, creates a
        string containing word and word's information, creates a text file, and writes all strings it.

        """
        line_to_index = ''
        for token in sorted(self.dictionary):
            line_to_index += (token + " " + str(self.dictionary[token]) + '\n')
        fp = open(os.path.join('SWE247P project', 'inv-index', cur_letter + '.txt'), 'w')
        fp.writelines(line_to_index)
        fp.close()
        print(line_to_index)


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
    files = []
    file_count = 0
    index = InvertedIndex()
    if not os.path.exists('SWE247P project/inv-index/temp_files'):
        os.mkdir('SWE247P project/inv-index/temp_files')
    for filename in glob.glob('SWE247P project/input-transform/**/*.txt', recursive=True):
        file_number = filename[-9:-4]
        files.append({'file_number': file_number, 'file_path': filename})
        with open(os.path.join(os.getcwd(), filename), 'r') as myfile:
            index.process_text(myfile, file_count)
        file_count += 1
    # write remaining entries
    index.write_partial_index()
    InvertedIndex().merge_inverted_index()
    os.rmdir('SWE247P project/inv-index/temp_files')

