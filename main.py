import sys
import time
from PDA import *
import typing


class HTMLParser(PDA):
    __errors: list
    _current_char: str
    file: typing.IO
    _current_line: int
    '''
    rest properties is at PDA class. @see PDA.py
    '''

    def __init__(self, pda_file):
        super().__init__(pda_file)
        # Now, PDA is ready to use.

        self.__errors = list()

    def check(self, html_file):
        start = time.time()

        print(
            f"Checking the HTML inside {html_file}\n")

        # Use additional function to maintain code readability
        self.__check_helper(html_file)

        # Now self.__errors is filled. We check whether there is some errors or not
        if self.is_accepted():
            print("Passed!")
        else:
            self.print_errors()

        duration = time.time() - start
        print(f"\nFinished in {duration} seconds.\n")

    def print_errors(self):
        err_length = len(self.__errors)
        for i in range(err_length):
            numline = self.__errors[i]["line"]
            message = self.__errors[i]["error_message"]

            print("Error in line {}: {}".format(numline, message))

    def _push_error(self, numline: int, error_message: str):
        self.__errors.append(
            {
                "line": numline,
                "error_message": error_message,
            }
        )

    def __check_helper(self, html_file):
        self.file = open(html_file, "r")
        self._current_char = None
        self._current_line = 1

        self.__next()
        self.__ignore_blanks()

        prev = self._current_char

        while (self._current_char != ""):

            if (self._current_char == "<"):
                self.__next()

                self.get_symbol("lb")
                self.epsilon_exploration()
                prev = "lb"
            elif (self._current_char == ">"):
                self.get_symbol("rb")
                self.epsilon_exploration()
                self.__next()
                prev = "rb"
            else:
                if (prev == 'lb'):
                    label_tag = self.read_label_tag()
                    self.get_symbol(label_tag)
                    self.epsilon_exploration()
                    prev = "labeltag"
                else:
                    self.get_symbol(self._current_char)
                    self.epsilon_exploration()
                    self.__next()

            self.__ignore_blanks()

        self.file.close()

    def __is_current_char_blank(self):
        return self._current_char == " " or self._current_char == '\n'

    def read_label_tag(self):
        # I.S. Sudah melewati '<', belum melewati '>', current char antara BLANK atau huruf pertama
        # F.S. membaca satu kata paling awal setelah '<',

        if self.__is_current_char_blank() or self._current_char == '>':
            self.__errors.append({
                "line": self._current_line,
                "error_message": "Expected a label tag, found nothing."
            })
            return None

        result = self._current_char
        self.__next()

        while (
                self._current_char != " " and
                self._current_char != ">" and
                self._current_char != "" and
                self._current_char != "\n" and
                self._current_char is not None):
            result += self._current_char
            self.__next()
        print(result)
        return result

    def __ignore_blanks(self):
        # Bukan cuma blanks sih, tapi juga \n.
        while self._current_char == " " or self._current_char == "\n":
            if (self._current_char == '\n'):
                self._current_line += 1
            self.__next()

    def read_double_quote(self):
        # return None kalo double quote ga ditutup
        double_quote_starts_line = self._current_line
        self.__next()

        if self._current_char == '\"':
            return ""

        val = ""

        while (self._current_char != '\"' and
               self._current_char is not None):
            if (self._current_char is None):
                self.__errors.append({
                    "line": double_quote_starts_line,
                    "error_message": "There is a double quote that doesn't have its closing double quote"
                })
                return None

            val += self._current_char
            self.__next()

        return val

    def read_attr(self):
        # I.S. Sudah melewati '<', belum melewati '>'
        # F.S. membaca satu kata paling awal setelah tag beserta isinya.
        # pita menunjuk ke character setelahnya, bisa " ", bisa ">", bisa "\n" atau bisa None (eof)

        # Contoh keluaran
        # img="hello world" -> ["img", "hello world"]
        # else, return None
        self.__ignore_blanks()

        if self._current_char == "=":
            self.__errors.append({
                "line": self._current_line,
                "error_message": "Unexpected character: '='"
            })
            return None

        curr_attr = ""

        while (
                self._current_char != " " and
                self._current_char != ">" and
                self._current_char != "" and
                self._current_char != "\n" and
                self._current_char != "=" and
                self._current_char is not None):

            if self._current_char == "\n":
                self._current_line += 1

            curr_attr += self._current_char
            self.__next()

        self.__ignore_blanks()
        if (self._current_char != "="):
            self.__errors.append({
                "line": self._current_line,
                "error_message": f"This attribute has no value: {curr_attr}"
            })
            return None

        self.__ignore_blanks()
        self.__next()
        if (self._current_char != "\""):
            self.__errors.append({
                "line": self._current_line,
                "error_message": f"Expected a value for attribute '{curr_attr}', but found something else."
            })
            return None

        val = self.read_double_quote()
        if val is None:
            return None

        return [curr_attr, val]

    def __next(self):
        self._current_char = self.file.read(1)


if __name__ == '__main__':
    pda_file = "pda.txt"
    html_file = "test/coba.html"

    parser2 = HTMLParser(pda_file)
    parser2.print_delta()
    parser2.check(html_file)
    print(parser2.filename)
