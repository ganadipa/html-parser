import sys
from PDA import *


class HTMLParser(PDA):
    __errors: list

    def __init__(self):
        self.__errors = list()
        self.__errors.append(
            {
                "line": 36,
                "error_message": "Can't help falling in love with you."
            }
        )

    def check(self, html_file, pda_file):
        print(
            f"Checking the HTML inside {html_file} given the PDA from {pda_file}...")

        if len(self.__errors) > 0:
            print("Passed!")
        else:
            self.print_errors()

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


if __name__ == '__main__':
    pda_file = sys.argv[1]
    html_file = sys.argv[2]

    parser = HTMLParser()
    parser.check(html_file, pda_file)
