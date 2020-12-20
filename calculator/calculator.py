import re
import math
from statistics import mean


# TODO: problem with negative number handling - to fix.


__token_specification = {
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
    'RIGHT_PARENTHESIS': r'\)'
}


__tok_regex = '|'.join('%s' % value for key, value in __token_specification.items())


def calculate(expression: str):
    if type(expression) is not str:
        raise TypeError("Expression input should be of str type.")

    expression = __remove_spaces(expression)

    return __calculate(expression)


def __remove_spaces(expression: str):
    return re.sub("\s", "", expression)


def __calculate(expression: str, result: int = 0):

    if __is_end_of_calculation(expression):
        return expression

    tmp_result = __handle_parenthesis(expression)
    if tmp_result is None:
        tmp_result = __handle_factorial(expression)
        if tmp_result is None:
            tmp_result = __handle_negate(expression)
            if tmp_result is None:
                tmp_result = __handle_max_min_average(expression)
                if tmp_result is None:
                    tmp_result = __handle_power(expression)
                    if tmp_result is None:
                        tmp_result = __handle_multiplication_division(expression)
                        if tmp_result is None:
                            tmp_result = __handle_addition_subtraction(expression)

    return __calculate(tmp_result)


def __is_end_of_calculation(expression: str):
    token = re.search(f'^(\w+|\w+\.\w+|-\w+|-\w+\.\w+)$', expression)

    if token is None:
        return False
    else:
        return True


def __handle_parenthesis(expression: str):
    token = re.search(f'{__token_specification["LEFT_PARENTHESIS"]}'
                      f'[^{__token_specification["LEFT_PARENTHESIS"]}{__token_specification["RIGHT_PARENTHESIS"]}]'
                      f'*{__token_specification["RIGHT_PARENTHESIS"]}',
                      expression)

    if token is None:
        return None
    else:
        return expression[:token.start():] + str(__calculate(expression[token.start() + 1:token.end() - 1:])) + \
               expression[token.end()::]


def __handle_factorial(expression: str):
    token = re.search(__token_specification["FACTORIAL"], expression)

    if token is None:
        return None
    else:
        result = math.factorial(int(expression[token.start() - 1:token.start():]))
        return expression[:token.start() - 1:] + str(math.factorial(int(expression[token.start() - 1:token.start():]))) + \
               expression[token.end()::]


def __handle_negate(expression: str):
    token = re.search(__token_specification["NEGATE"], expression)

    if token is None:
        return None
    else:
        return expression[:token.start():] + str(-1 * int(expression[token.end():token.end() + 1:])) + \
               expression[token.end() + 1::]


def __handle_max_min_average(expression: str):
    token = re.search(f'(\w+)([{__token_specification["MAX"]}{__token_specification["MIN"]}'
                      f'{__token_specification["AVERAGE"]}])(\w+)', expression)

    if token is None:
        return None
    else:
        if token.group(2) == '$':
            result = max(int(token.group(1)), int(token.group(3)))
        elif token.group(2) == '&':
            result = min(int(token.group(1))), int(token.group(3))
        else:
            result = mean([int(token.group(1)), int(token.group(3))])

    return expression[:token.start():] + str(result) + expression[token.end()::]


def __handle_power(expression: str):
    token = re.search(__token_specification["POWER"], expression)

    if token is None:
        return None
    else:
        return expression[:token.start() - 1:] + \
               str(int(expression[token.start() - 1:token.start():]) ** int(expression[token.end():token.end() + 1:])) \
               + expression[token.end() + 1::]


def __handle_multiplication_division(expression: str):
    token = re.search(f'(\w+)([{__token_specification["MULTIPLICATION"]}{__token_specification["DIVISION"]}])(\w+)', expression)

    if token is None:
        return None
    else:
        if token.group(2) == '*':
            result = int(token.group(1)) * int(token.group(3))
        else:
            result = int(token.group(1)) / int(token.group(3))

    return expression[:token.start():] + str(result) + expression[token.end()::]


def __handle_addition_subtraction(expression: str):
    token = re.search(f'(\w+)([{__token_specification["ADDITION"]}{__token_specification["SUBTRACTION"]}]+)(\w+)',
                      expression)

    if token is None:
        return None
    else:
        if token.group(2) == '+':
            result = int(token.group(1)) + int(token.group(3))
        else:
            result = int(token.group(1)) - int(token.group(3))

    return expression[:token.start():] + str(result) + expression[token.end()::]


exp = "1 * 3 @ 7 - (24 + ((5 - 3) + 2)) + 4 + (3! + ~3 + 7) + 5 ^ 2"
# exp = "2 + 4 * 4 * 2"
print(calculate(exp))
