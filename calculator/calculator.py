import re
import math
from statistics import mean
from typing import Union


__TOKEN_SPECIFICATION = {
    'ADDITION': r'\+',
    'SUBTRACTION': r'-',
    'MULTIPLICATION': r'\*',
    'DIVISION': r'/',
    'POWER': r'\^',
    'NEGATE': r'~',
    'MODULE': r'%',
    'FACTORIAL': r'!',
    'AVERAGE': r'@',
    'MAX': r'\$',
    'MIN': r'&',
    'LEFT_PARENTHESIS': r'\(',
    'RIGHT_PARENTHESIS': r'\)',
    'NUMBER': '\w+',
    'NUMBER_FLOAT': '\w+\.\w+',
}

__NUMBER_REGEX = f'{__TOKEN_SPECIFICATION["SUBTRACTION"]}{__TOKEN_SPECIFICATION["NUMBER_FLOAT"]}|' \
                 f'{__TOKEN_SPECIFICATION["SUBTRACTION"]}{__TOKEN_SPECIFICATION["NUMBER"]}|' \
                 f'{__TOKEN_SPECIFICATION["NUMBER_FLOAT"]}|' \
                 f'{__TOKEN_SPECIFICATION["NUMBER"]}'

__OPERATION_HANDLERS = (
    "__handle_parenthesis",
    "__handle_factorial",
    "__handle_negate",
    "__handle_max_min_average",
    "__handle_power",
    "__handle_multiplication_division",
    "__handle_addition_subtraction",
)


def calculate(expression: str) -> Union[int, float]:
    if type(expression) is not str:
        raise TypeError("Expression input should be of str type.")

    return __calculate(re.sub("\s", "", expression))


def __calculate(expression: str) -> Union[int, float]:
    if __is_end_of_calculation(expression):
        return expression

    for func in __OPERATION_HANDLERS:
        tmp_result = eval(func)(expression)
        if tmp_result is None:
            continue
        else:
            return __calculate(tmp_result)

    raise ValueError(f'Expression: {expression} is not legal!')


def __is_end_of_calculation(expression: str) -> bool:
    if re.search(f'^({__NUMBER_REGEX})$', expression):
        return True

    return False


def __handle_parenthesis(expression: str) -> str:
    token = re.search(f'{__TOKEN_SPECIFICATION["LEFT_PARENTHESIS"]}'
                      f'([^{__TOKEN_SPECIFICATION["LEFT_PARENTHESIS"]}{__TOKEN_SPECIFICATION["RIGHT_PARENTHESIS"]}]*)'
                      f'{__TOKEN_SPECIFICATION["RIGHT_PARENTHESIS"]}',
                      expression)

    if token:
        return expression[:token.start():] + str(__calculate(token.group(1))) + expression[token.end()::]

    return None


def __handle_factorial(expression: str) -> str:
    token = re.search(f'({__NUMBER_REGEX}){__TOKEN_SPECIFICATION["FACTORIAL"]}', expression)

    if token:
        return expression[:token.start():] + str(math.factorial(float(token.group(1)))) + expression[token.end()::]

    return None


def __handle_negate(expression: str) -> str:
    token = re.search(f'({__NUMBER_REGEX}){__TOKEN_SPECIFICATION["NEGATE"]}', expression)

    if token:
        return expression[:token.start():] + str(-1 * float(token.group(1))) + expression[token.end()::]

    return None


def __handle_max_min_average(expression: str) -> str:
    token = re.search(f'({__NUMBER_REGEX})'
                      f'([{__TOKEN_SPECIFICATION["MAX"]}{__TOKEN_SPECIFICATION["MIN"]}'
                      f'{__TOKEN_SPECIFICATION["AVERAGE"]}])'
                      f'({__NUMBER_REGEX})',
                      expression)

    if token:
        if token.group(2) == '$':
            result = max(float(token.group(1)), float(token.group(3)))
        elif token.group(2) == '&':
            result = min(float(token.group(1)), float(token.group(3)))
        else:
            result = mean([float(token.group(1)), float(token.group(3))])

        return expression[:token.start():] + str(result) + expression[token.end()::]

    return None


def __handle_power(expression: str) -> str:
    token = re.search(f'({__NUMBER_REGEX}){__TOKEN_SPECIFICATION["POWER"]}({__NUMBER_REGEX})', expression)

    if token:
        return expression[:token.start():] + str(float(token.group(1)) ** float(token.group(2))) + expression[token.end()::]

    return None


def __handle_multiplication_division(expression: str) -> str:
    token = re.search(f'({__NUMBER_REGEX})'
                      f'([{__TOKEN_SPECIFICATION["MULTIPLICATION"]}{__TOKEN_SPECIFICATION["DIVISION"]}])'
                      f'({__NUMBER_REGEX})',
                      expression)

    if token:
        if token.group(2) == '*':
            result = float(token.group(1)) * float(token.group(3))
        else:
            result = float(token.group(1)) / float(token.group(3))

        return expression[:token.start():] + str(result) + expression[token.end()::]

    return None


def __handle_addition_subtraction(expression: str) -> str:
    token = re.search(f'({__NUMBER_REGEX})'
                      f'([{__TOKEN_SPECIFICATION["ADDITION"]}{__TOKEN_SPECIFICATION["SUBTRACTION"]}])'
                      f'({__NUMBER_REGEX})',
                      expression)

    if token:
        if token.group(2) == '+':
            result = float(token.group(1)) + float(token.group(3))
        else:
            result = float(token.group(1)) - float(token.group(3))

        return expression[:token.start():] + str(result) + expression[token.end()::]

    return None
