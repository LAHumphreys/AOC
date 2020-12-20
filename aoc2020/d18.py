import copy
import re
from enum import Enum

number = re.compile("^ *([0-9])+(.*)$")


class UnknownOperation(Exception):
    pass


class LogicError(Exception):
    pass


class Operation(Enum):
    ASSIGN = 1,
    ADD = 2
    MULTIPLY = 3
    POP = 4


class PopMode(Enum):
    AUTO = 1,
    EXPLICIT = 2


def add_brackets(equation):
    return equation




LHS_PRECEDENCE = {
    Operation.ADD: 1,
    Operation.MULTIPLY: 1,
    Operation.ASSIGN: 99,
    Operation.POP: -1,
}
ADD_FIRST_PRECDENCE = {
    Operation.ADD: 1,
    Operation.MULTIPLY: 0,
    Operation.ASSIGN: 99,
    Operation.POP: -1,
}

def stack_calculator(equation):
    return stack_calculator_precedence(equation, precedence=LHS_PRECEDENCE)

def stack_calculator_precedence(equation, precedence = ADD_FIRST_PRECDENCE):
    stack = []

    lhs = None
    rhs = None
    op = Operation.ASSIGN
    next_op = None

    def apply_operator():
        popped = False
        nonlocal op, lhs, rhs
        if op == Operation.ASSIGN:
            lhs = rhs
        elif op == Operation.ADD:
            lhs += rhs
        elif op == Operation.MULTIPLY:
            lhs *= rhs
        elif op == Operation.POP:
            popped = True
            rhs = lhs
            lhs, op, _ = stack.pop()
        else:
            raise UnknownOperation
        return popped

    while equation != "":
        equation = equation.strip()
        number_match = re.match(number, equation)
        if number_match:
            equation = number_match.group(2)
            rhs = int(number_match.group(1))
        else:
            advance = 1
            if equation[0] == "+":
                next_op = Operation.ADD
            elif equation[0] == "*":
                next_op = Operation.MULTIPLY
            elif equation[0] == "(":
                stack.append((lhs, op, PopMode.EXPLICIT))
                lhs = None
                op = Operation.ASSIGN
            elif equation[0] == ")":
                next_op = Operation.POP
            else:
                raise UnknownOperation

            if next_op is not None:
                if len(stack) > 0 and stack[-1][2] == PopMode.AUTO:
                    stacked_op = stack[-1][1]
                    if precedence[stacked_op] >= precedence[next_op]:
                        next_op = Operation.POP
                        advance = 0

                if precedence[next_op] > precedence[op]:
                    stack.append((lhs, op, PopMode.AUTO))
                    lhs = None
                    op = Operation.ASSIGN

            equation = equation[advance:]

        while op == Operation.POP or (rhs is not None and next_op is not None):
            popped = apply_operator()

            if popped:
                pass
            else:
                op = next_op
                rhs = None
                next_op = None

        while rhs is not None and equation == "":
            popped = apply_operator()

            if popped:
                pass
            elif equation == "" and len(stack) > 0 and next_op != Operation.POP:
                op = Operation.POP
            else:
                op = next_op
                rhs = None
                next_op = None

    if len(stack) != 0:
        raise LogicError

    return lhs


if __name__ == "__main__":
    def main():
        with open("input/d18.txt") as file:
            equations = file.read().split("\n")
            sum = 0
            precedence_sum = 0
            for equation in equations:
                sum += stack_calculator(copy.copy(equation))
                precedence_sum += stack_calculator_precedence(copy.copy(equation))
        print("Sum of all equations: {0}".format(sum))
        print("Sum of all equations (predence): {0}".format(precedence_sum))


    main()
