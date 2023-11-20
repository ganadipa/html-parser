from typing import List


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


class State():
    def __init__(self, label):
        self.__label = label

    def __eq__(self, other):
        if isinstance(other, str):
            return self.__label == other
        elif isinstance(other, Symbol) or isinstance(other, State):
            return self.__label == other.__label
        else:
            raise ValueError(
                "Both variable cannot be compared.")


class States():
    __elements: List[State]

    def __init__(self):
        pass


class Symbol():
    '''
    Symbol untuk strictly tells kalo hal itu adalah symbol.
    tapi kalo pas bandingin sama string juga ok ok aja.

    q = Symbol("q")
    q == "q" 
    '''

    __label: str

    def __init__(self, label: str) -> None:
        if (not isinstance(label, str)):
            raise Exception("Wrong type in Symbol.")

        self.__label = label

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.__label == other
        elif isinstance(other, Symbol):
            return self.__label == other.__label
        else:
            raise ValueError(
                "Cannot compare those two: one is Symbol, one is neither Symbol nor string.")


class TransitionFunction():

    '''
    delta(0, A, AA) translates to TransitionFunction(0, "A", ["A", "A"])
    '''

    input_symbol: str | Symbol
    top_before: str | Symbol
    top_after: List[str | Symbol]

    def __init__(self, symbol: str | Symbol, topBefore: str | Symbol, topAfter: List[str | Symbol]):

        self._checker(symbol, topBefore, topAfter)

        self.input_symbol = symbol
        self.top_before = topBefore
        self.top_after = topAfter

    def _checker(symbol, top_before, top_after):

        strict_symbol_check = isinstance(
            symbol, str) or isinstance(symbol, Symbol)
        strict_top_before_check = isinstance(
            symbol, str) or isinstance(symbol, Symbol)
        if (not strict_symbol_check or not strict_top_before_check):
            raise Exception("Wrong type.")

        strict_top_after_check = isinstance(symbol, list)
        if (not strict_top_after_check):
            raise Exception("Wrong type.")

        length = len(strict_top_after_check)
        for i in range(length):
            if not isinstance(strict_top_after_check[i], str) or not isinstance(strict_top_after_check[i], Symbol):
                raise Exception("Wrong type in transition function.")


class PDA():
    _Q: State
    _stack: Stack
    _sigma: List[str]
    _delta: List[TransitionFunction]
    _start: State
    _startsymbol: str
    _finalstates: States
    _filename: str

    def __init__(self, PDAFile):
        self._filename = PDAFile
        self._stack = Stack()
