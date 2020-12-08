import re
from collections import namedtuple

from utils.test_case import TestCase
from d8_input import INPUT

TEST_CASES = [
    TestCase("""
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""", 8),
]

Instruction = namedtuple('Instruction', 'operation argument')


def parse_instruction(line):
    operation, argument = re.match(r'(acc|jmp|nop) ([-+]?\d+)', line).groups()
    argument = int(argument, 10)
    return Instruction(operation, argument)


def run(program):

    accumulator = 0
    pc = 0
    already_executed = set()

    while True:
        if pc in already_executed:
            return False
        if pc >= len(program):
            return accumulator
        already_executed.add(pc)
        current = program[pc]
        if current.operation == 'acc':
            accumulator += current.argument
            pc += 1
        elif current.operation == 'jmp':
            pc += current.argument
        elif current.operation == 'nop':
            pc += 1
        else:
            assert False, 'bad instruction'

def solve(input):
    program = [
        parse_instruction(line)
        for line in input.strip().split('\n')
    ]

    result = run(program)
    if result:
        return result

    for i, instruction in enumerate(program):
        if instruction.operation in ('jmp', 'nop'):
            modified_program = program.copy()
            modified_program[i] = Instruction('nop' if instruction.operation == 'jmp' else 'jmp', instruction.argument)
            result = run(modified_program)
            if result:
                return result

    return None


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        case.check(result)

    print(solve(INPUT))
