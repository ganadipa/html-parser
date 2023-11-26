from typing import List


def stringToListOfTag(string: str) -> List[str]:
    # I.S Pokonya stringnya ga boleh ngaco.

    # Contoh input
    # <hello> -> ["<hello>"]
    # <hello><world> -> ["<hello>", "<world>"]

    tags = string.split("><")
    for i in range(len(tags)):
        tags[i] = tags[i].replace("<", "")
        tags[i] = tags[i].replace(">", "")
        tags[i] = "<" + tags[i] + ">"

    return tags


class Stack():
    __elements: List

    def __init__(self):
        self.__elements = list()

    def top(self) -> any:
        if (self.is_empty()):
            return "<e>"
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

    def is_empty(self) -> bool:
        return len(self.__elements) == 0

    def __str__(self) -> None:
        for i in range(self.height()):
            print(self.__elements[i])

    def __len__(self) -> int:
        return self.height()

    def __eq__(self, stock) -> bool:
        if (len(self) != len(stock)):
            return False
        else:
            return self.__elements == stock.__elements


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

    def __str__(self):
        return f"delta({self.state_before}, {self.input_symbol}, {self.top_before}) = ({self.state_after}, {self.top_after})"


class PDAstate():
    state: str
    stack: Stack

    def __init__(self, state, stack_top):
        self.state = state
        self.stack = Stack()
        self.stack.push(stack_top)

    def copy_self(self):
        newPDAState = PDAstate(self.state, "<>")
        newStack = Stack()

        for i in range(len(self.stack)):
            newStack.push(self.stack.info(i))

        newPDAState.stack = newStack
        return newPDAState

    def transition(self, input_symbol, transition_function):
        i_symbol_check = (transition_function.input_symbol == '%'
                          and input_symbol not in ['lb', 'rb', '/', '"', "'"])
        i_symbol_check2 = (transition_function.input_symbol == '$'
                           and input_symbol not in ['lb', 'rb'])
        is_symbol_match = (transition_function.input_symbol ==
                           input_symbol) or (i_symbol_check) or (i_symbol_check2)

        if (transition_function.state_before[-1] == "*"):
            prefix = transition_function.state_before.split("*")[0]
            matching_state = self.state.startswith(prefix)
            star = self.state.removeprefix(prefix)
            ending_state = transition_function.state_after.replace("*", star)
        else:
            matching_state = transition_function.state_before == self.state
            ending_state = transition_function.state_after

        if (
            is_symbol_match and
            matching_state and
            transition_function.top_before == self.stack.top()
        ):
            result = self.copy_self()
            result.state = ending_state

            result.stack.pop()
            for i in transition_function.top_after[::-1]:
                if (i != "<e>"):
                    result.stack.push(i)
            return result
        return False

    def __eq__(self, friend):
        if (self.state != friend.state):
            return False
        if (self.stack != friend.stack):
            return False
        return True


class PDA():
    Q: List[str]
    stack: Stack
    alphabet: List[str]  # input symbols
    delta: List[TransitionFunction]  # transition functions
    start_state: str
    stack_symbols: List[str]
    start_symbol: str  # Initial stack symbol
    final_states: List[str]
    by_empty_stack: bool
    filename: str

    current_states: List[PDAstate]

    def __init__(self, PDAFile):
        self.filename = PDAFile
        self.stack = Stack()
        self.delta = list()
        self.Q = list()
        self.alphabet = list()
        self.stack_symbols = list()
        self.final_states = list()

        with open(PDAFile, "r") as f:

            states_line = f.readline().strip()

            states = states_line.split(" ")
            for state in states:
                self.add_state(state)

            input_symbols_line = f.readline().strip()
            i_symbols = input_symbols_line.split(" ")
            for symbol in i_symbols:
                self.add_alphabet(symbol)

            stack_symbols_line = f.readline().strip()
            s_symbols = stack_symbols_line.split(" ")
            for symbol in s_symbols:
                self.add_stack_symbols(symbol)

            self.start_state = f.readline().strip()

            self.start_symbol = f.readline().strip()

            final_states_line = f.readline().strip()
            f_states = final_states_line.split(" ")
            for state in f_states:
                self.add_final_states(state)

            self.by_empty_stack = f.readline().strip() == "E"

            #
            # Rest is entries of transition functions
            transition_function_line = f.readline()
            while transition_function_line != "":
                if (transition_function_line == '\n'):
                    transition_function_line = f.readline()
                    continue
                transition_function_line = transition_function_line.split("#")[
                    0]

                if len(transition_function_line) <= 8:
                    transition_function_line = f.readline()
                    continue

                transition_function_line = transition_function_line.strip()
                t_function = transition_function_line.split(" ")

                bef_state = t_function[0]
                input_symbol = t_function[1]
                bef_top_stack = t_function[2]
                aft_state = t_function[3]
                aft_top_stack = stringToListOfTag(t_function[4])

                d = TransitionFunction(
                    input_symbol, bef_top_stack, aft_top_stack, bef_state, aft_state)

                self.add_delta(d)

                transition_function_line = f.readline()

        self.current_states = [PDAstate(self.start_state, self.start_symbol)]

    def add_state(self, state: str):
        self.Q.append(state)

    def add_alphabet(self, symbol: str):
        self.alphabet.append(symbol)

    def add_delta(self, tf: TransitionFunction):
        self.delta.append(tf)

    def add_stack_symbols(self, symb: str):
        self.stack_symbols.append(symb)

    def add_final_states(self, state: str):
        self.final_states.append(state)

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

    def get_symbol(self, symbol):

        next_states = list()
        for state in self.current_states:
            for transition_function in self.delta:
                if (state.transition(symbol, transition_function)):
                    next_states.append(state.transition(
                        symbol, transition_function))
        if (symbol == "eps"):
            for state in next_states:
                if (state not in self.current_states):
                    self.current_states.append(state)
        else:
            self.current_states = next_states

    def is_accepted(self):
        if self.by_empty_stack:
            for state in self.current_states:
                if (state.stack.is_empty()):
                    return True
            return False
        else:
            for state in self.current_states:
                if (state.state in self.final_states):
                    return True
            return False

    def epsilon_exploration(self):
        epsilon_try = True
        while (epsilon_try and len(self.current_states) != 0):
            last_state = []
            for state in self.current_states:
                last_state.append(state.copy_self())
            self.get_symbol("eps")
            if (len(last_state) != len(self.current_states)):
                pass
            else:
                for i in range(len(last_state)):
                    epsilon_try = False
                    if (not (last_state[i] == self.current_states[i])):
                        epsilon_try = True

    def is_tape_accepted(self, tape):
        self.epsilon_exploration()
        for symbol in tape:
            self.get_symbol(symbol)
            self.epsilon_exploration()
        return self.is_accepted()

    def print_states_from_delta(self):
        seen = []
        for tf in self.delta:
            bef_state = tf.state_before
            aft_state = tf.state_after

            if bef_state not in seen:
                seen.append(bef_state)

            if (aft_state not in seen):
                seen.append(aft_state)

        for i in seen:
            print(i, end=" ")
        print()

    def print_input_symbol_from_delta(self):
        seen = []
        for tf in self.delta:
            inp = tf.input_symbol

            if inp not in seen:
                seen.append(inp)

        for i in seen:
            print(i, end=" ")
        print()

    def print_stack_symbol_from_delta(self):
        seen = []
        for tf in self.delta:
            stack_before = tf.top_before

            if stack_before not in seen:
                seen.append(stack_before)

        for i in seen:
            print(i, end=" ")
        print()


# pathPDA = "config.txt"
# tape = "0101101010"
# tape = tape + tape[::-1] + "1"
# print(tape)
# gana = PDA(pathPDA)
# print(gana.is_tape_accepted(tape))
