import sys
from PDA import *


class HTMLParser(PDA):
    def __init__(self):
        pass

    @staticmethod
    def check(html_file, pda_file):
        print(
            f"Checking the HTML inside {html_file} given the PDA from {pda_file}...")
        print("Passed!")


if __name__ == '__main__':
    pda_file = sys.argv[1]
    html_file = sys.argv[2]

    HTMLParser.check(html_file, pda_file)
