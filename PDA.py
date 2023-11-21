from typing import List


def stringToListOfTag(string: str) -> List[str]:
    # I.S Pokonya stringnya ga boleh ngaco.

    # Contoh input
    # <hello> -> ["hello"]
    # <hello><world> -> ["<hello>", "<world>"]

    result = list()

    tags = string.split("><")
    for i in range(len(tags)):
        if (i == 0):
            tags[i] = tags[i] + '>'
            continue
        if (i == len(tags) - 1):
            tags[i] = '<' + tags[i]
            continue

        tags[i] = '<' + tags[i] + '>'

    return tags


class Stack():
    __elements: List

    def __init__(self):
        self.__elements = list()

    def top(self) -> any:
        return self.__elements[-1]

    def push(self, value: any):
        self.__elements.append(value)

    def pop(self) -> any:
        return self.__elements.pop()

    def info(self, index) -> any:
        # return a value in the stack where index = 0 means it is at the stop of the stack
        return self.__elements[index]

    def height(self) -> int:
        return len(self.__elements)

    def __str__(self) -> None:
        for i in range(self.height()):
            print(self.__elements[i])

    def __len__(self) -> int:
        return self.height()


class TransitionFunction():

    '''
    delta(q, 0, A) = (q, B)
    '''

    input_symbol: str
    top_before: str
    top_after: List[str]
    state_before: str
    state_after: str

    def __init__(self, symbol: str, topBefore: str, topAfter: List[str], stateBefore, stateAfter):

        self.input_symbol = symbol
        self.top_before = topBefore
        self.state_before = stateBefore
        self.top_after = topAfter
        self.state_after = stateAfter

    # def _checker(symbol, top_before, top_after):

    #     strict_top_after_check = isinstance(symbol, list)
    #     if (not strict_top_after_check):
    #         raise Exception("Wrong type.")

    #     length = len(strict_top_after_check)
    #     for i in range(length):
    #         if not isinstance(strict_top_after_check[i], str):
    #             raise Exception("Wrong type in transition function.")

    def __str__(self):
        return f"delta({self.state_before}, {self.input_symbol}, {self.top_before}) = ({self.state_after}, {self.top_after})"


class PDA():
    Q: List[str]
    stack: Stack
    sigma: List[str]  # input symbols
    delta: List[TransitionFunction]  # transition functions
    start: str
    stack_symbols: List[str]
    start_symbol: str  # Initial stack symbol
    finalstates: List[str]
    byemptystack: bool
    filename: str

    def __init__(self, PDAFile):
        self.filename = PDAFile
        self.stack = Stack()
        self.delta = list()
        self.Q = list()
        self.sigma = list()
        self.stack_symbols = list()
        self.finalstates = list()

        with open(PDAFile, "r") as f:

            states_line = f.readline()[:-1]

            states = states_line.split(" ")
            for state in states:
                self.add_state(state)

            input_symbols_line = f.readline()[:-1]
            i_symbols = input_symbols_line.split(" ")
            for symbol in i_symbols:
                self.add_sigma(symbol)

            stack_symbols_line = f.readline()[:-1]
            s_symbols = stack_symbols_line.split(" ")
            for symbol in s_symbols:
                self.add_stack_symbols(symbol)

            self.start = f.readline()[:-1]

            self.startsymbol = f.readline()[:-1]

            final_states_line = f.readline()[:-1]
            f_states = final_states_line.split(" ")
            for state in f_states:
                self.add_final_states(state)

            self.byemptystack = f.readline()[:-1] == "E"

            #
            # Rest is entries of transition functions
            transition_function_line = f.readline()[:-1]
            while transition_function_line != "":
                t_function = transition_function_line.split(" ")

                bef_state = t_function[0]
                input_symbol = t_function[1]
                bef_top_stack = t_function[2]
                aft_state = t_function[3]
                aft_top_stack = stringToListOfTag(t_function[4])

                d = TransitionFunction(
                    input_symbol, bef_top_stack, aft_top_stack, bef_state, aft_state)

                self.add_delta(d)

                transition_function_line = f.readline()[:-1]

    def add_state(self, state: str):
        self.Q.append(state)

    def add_sigma(self, symbol: str):
        self.sigma.append(symbol)

    def add_delta(self, tf: TransitionFunction):
        self.delta.append(tf)

    def add_stack_symbols(self, symb: str):
        self.stack_symbols.append(symb)

    def add_final_states(self, state: str):
        self.finalstates.append(state)

    def print_delta(self):
        for i in range(len(self.delta)):
            print(self.delta[i])

    def print_all(self):
        print(f'Q: ', self.Q)
        print(f'Stack: \n', self.stack)
        print(f'Delta: ', self.delta)

    def push_stack(self, symbol):
        self.stack.push(symbol)

    def pop_stack(self):
        return self.stack.pop()
