class EquationState(object):
    def __init__(self, equation_string, moves=0):
        self._moves = moves
        self._numbers = []
        self._operators = []
        for i, c in enumerate(equation_string):
            if c.isdigit():
                self._numbers.append(int(c))
            elif c == '=':
                self._eq_pos = len(self._numbers)
            else:
                self._operators.append(c)

    def __setitem__(self, key, value):
        self._numbers[key] = value

    def __getitem__(self, item):
        return self._numbers[item]

    def __str__(self):
        state_string = ""
        op_count = 0
        for i, n in enumerate(self._numbers):
            state_string += str(n)
            if i == self._eq_pos - 1:
                state_string += "="
            elif op_count < len(self._operators):
                state_string += self._operators[op_count]
                op_count += 1
        return state_string

    def __repr__(self):
        return f"<{str(self)}:{self._moves}>"

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def check(self):
        calc_list = [self._numbers[0], self._numbers[-1]]
        for i, op in enumerate(self._operators):
            if op == "+":
                calc_list.append(self._numbers[i + 1])
            elif op == "-":
                calc_list.append(- self._numbers[i + 1])
        for i, n in enumerate(calc_list):
            if i >= self._eq_pos:
                calc_list[i] = -n
        return (sum(calc_list) % 10) == 0

    def copy(self):
        return EquationState(str(self), self._moves + 1)


state_transitions = {
    0: {
        "mov": [9, 6],
        "add": [8],
        "rem": []
    },
    1: {
        "mov": [],
        "add": [7],
        "rem": []
    },
    2: {
        "mov": [3],
        "add": [],
        "rem": []
    },
    3: {
        "mov": [2, 5],
        "add": [9],
        "rem": []
    },
    4: {
        "mov": [],
        "add": [],
        "rem": []
    },
    5: {
        "mov": [3],
        "add": [6, 9],
        "rem": []
    },
    6: {
        "mov": [9, 0],
        "add": [8],
        "rem": [5]
    },
    7: {
        "mov": [],
        "add": [],
        "rem": [1]
    },
    8: {
        "mov": [],
        "add": [],
        "rem": [0, 6, 9]
    },
    9: {
        "mov": [6, 0],
        "add": [8],
        "rem": [5, 3]
    }
}


def solution_search(base_equation, max_level):
    solution_candidates = [base_equation]

    additional_candidates = []
    previous_candidates = [base_equation]

    for level in range(1, max_level + 1, 1):
        for prev_sol in previous_candidates:
            for i, val in enumerate(prev_sol):
                for replacement in state_transitions[val]["mov"]:
                    mov_state = prev_sol.copy()
                    mov_state[i] = replacement
                    if mov_state not in solution_candidates:
                        additional_candidates.append(mov_state)
                        solution_candidates.append(mov_state)
                for removal in state_transitions[val]["rem"]:
                    for j, other in enumerate(prev_sol):
                        if i == j:
                            continue
                        else:
                            for inner_addition in state_transitions[other]["add"]:
                                rem_state = prev_sol.copy()
                                rem_state[i] = removal
                                rem_state[j] = inner_addition
                                if rem_state not in solution_candidates:
                                    additional_candidates.append(rem_state)
                                    solution_candidates.append(rem_state)
                for addition in state_transitions[val]["add"]:
                    for j, other in enumerate(prev_sol):
                        if i == j:
                            continue
                        else:
                            for inner_removal in state_transitions[other]["rem"]:
                                add_state = prev_sol.copy()
                                add_state[i] = addition
                                add_state[j] = inner_removal
                                if add_state not in solution_candidates:
                                    additional_candidates.append(add_state)
                                    solution_candidates.append(add_state)
        previous_candidates = additional_candidates.copy()
        additional_candidates = []

    return solution_candidates


if __name__ == '__main__':
    teststate = EquationState("1+2=3+4")
    print(teststate.check())
    print([sol for sol in solution_search(teststate, 3) if sol.check()])
