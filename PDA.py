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
    __label: str

    def __init__(self, label: str) -> None:
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
    def __init__(self):
        pass


class PDA():
    __Q: State
    __stack: Stack
    __sigma: List[str]
    __delta: List[TransitionFunction]
    __start: State
    __startsymbol: str
    __finalstates: States

    def __init__(self, PDAFile):

        self.__stack = Stack()
