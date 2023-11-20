import sys
import time
from PDA import *


class HTMLParser(PDA):
    __errors: list
    '''
    rest properties is at PDA class. @see PDA.py
    '''

    def __init__(self, pda_file):
        super().__init__(pda_file)
        # Now, PDA is ready to use.

        self.__errors = list()
        self.__errors.append(
            {
                "line": 36,
                "error_message": "Can't help falling in love with you."
            }
        )

    def check(self, html_file):
        start = time.time()

        print(
            f"Checking the HTML inside {html_file}\n")

        # Use additional function to maintain code readability
        self.__check_helper(html_file)

        # Now self.__errors is filled. We check whether there is some errors or not
        if len(self.__errors) <= 0:
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
        pass


if __name__ == '__main__':
    pda_file = sys.argv[1]
    html_file = sys.argv[2]

    parser1 = HTMLParser(pda_file + "2")
    parser2 = HTMLParser(pda_file)
    parser1.check(html_file)
    parser2.check(html_file)
    print(parser1._filename)
    print(parser2._filename)
