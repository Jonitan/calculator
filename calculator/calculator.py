import re
import math
from typing import Union
from statistics import mean


__TOKEN_SPECIFICATION = {
    'ADDITION': r'(?P<ADDITION>\+)',
    'SUBTRACTION': r'(?P<SUBTRACTION>-)',
    'MULTIPLICATION': r'(?P<MULTIPLICATION>\*)',
    'DIVISION': r'(?P<DIVISION>/)',
    'POWER': r'(?P<POWER>\^)',
    'NEGATE': r'(?P<NEGATE>~)',
    'MODULE': r'(?P<MODULE>%)',
    'FACTORIAL': r'(?P<FACTORIAL>!)',
    'AVERAGE': r'(?P<AVERAGE>@)',
    'MAX': r'(?P<MAX>\$)',
    'MIN': r'(?P<MIN>&)',
    'LEFT_PARENTHESIS': r'\(',
    'RIGHT_PARENTHESIS': r'\)',
    'NUMBER': '\d+(?:\.\d+)?',
    'NUMBER_NEGATIVE_OPT': '-?\d+(?:\.\d+)?',
}


def calculate(expression: str) -> Union[int, float]:
    if type(expression) is not str:
        raise TypeError("Expression input should be of str type.")

    return __calculate(re.sub("\s", "", expression))

def __calculate(expression: str) -> Union[int, float]:
    if __is_end_of_calculation(expression):
        return expression

    for func in __OPERATION_HANDLERS:
        tmp_result = func(expression)
        if tmp_result is not None:
            return __calculate(tmp_result)

    raise ValueError(f'Expression: {expression} is not legal!')

def __is_end_of_calculation(expression: str) -> bool:
    return re.fullmatch(f'{__TOKEN_SPECIFICATION["NUMBER_NEGATIVE_OPT"]}', expression) is not None

def __handle_parenthesis(expression: str) -> str:
    token = re.search(f'{__TOKEN_SPECIFICATION["LEFT_PARENTHESIS"]}'
                      f'([^{__TOKEN_SPECIFICATION["LEFT_PARENTHESIS"]}{__TOKEN_SPECIFICATION["RIGHT_PARENTHESIS"]}]*)'
                      f'{__TOKEN_SPECIFICATION["RIGHT_PARENTHESIS"]}',
                      expression)

    if token:
        return re.sub(token.re, str(__calculate(token.group(1))), expression, 1)

    return None

def __handle_factorial(expression: str) -> str:
    token = re.search(f'(?P<NUMBER>{__TOKEN_SPECIFICATION["NUMBER"]}){__TOKEN_SPECIFICATION["FACTORIAL"]}', expression)

    if token:
        return re.sub(token.re, str(math.factorial(float(token.group("NUMBER")))), expression, 1)

    return None

def __handle_negate(expression: str) -> str:
    token = re.search(f'(?P<NUMBER>{__TOKEN_SPECIFICATION["NUMBER"]}){__TOKEN_SPECIFICATION["NEGATE"]}', expression)

    if token:
        return re.sub(token.re, str(-1 * float(token.group("NUMBER"))), expression, 1)

    return None

def __handle_max_min_average(expression: str) -> str:
    token = re.search(f'(?P<FIRST_NUMBER>{__TOKEN_SPECIFICATION["NUMBER_NEGATIVE_OPT"]})'
                      f'({__TOKEN_SPECIFICATION["MAX"]}|{__TOKEN_SPECIFICATION["MIN"]}|'
                      f'{__TOKEN_SPECIFICATION["AVERAGE"]})'
                      f'(?P<SECOND_NUMBER>{__TOKEN_SPECIFICATION["NUMBER_NEGATIVE_OPT"]})',
                      expression)

    if token:
        if token.group("MAX"):
            result = max(float(token.group("FIRST_NUMBER")), float(token.group("SECOND_NUMBER")))
        elif token.group("MIN"):
            result = min(float(token.group("FIRST_NUMBER")), float(token.group("SECOND_NUMBER")))
        else:
            result = mean([float(token.group("FIRST_NUMBER")), float(token.group("SECOND_NUMBER"))])

        return re.sub(token.re, str(result), expression, 1)

    return None

def __handle_power(expression: str) -> str:
    token = re.search(f'(?P<FIRST_NUMBER>{__TOKEN_SPECIFICATION["NUMBER_NEGATIVE_OPT"]})'
                      f'{__TOKEN_SPECIFICATION["POWER"]}'
                      f'(?P<SECOND_NUMBER>{__TOKEN_SPECIFICATION["NUMBER_NEGATIVE_OPT"]})',
                      expression)

    if token:
        return re.sub(token.re, str(float(token.group("FIRST_NUMBER")) ** float(token.group("SECOND_NUMBER"))),
                      expression, 1)

    return None

def __handle_multiplication_division(expression: str) -> str:
    token = re.search(f'(?P<FIRST_NUMBER>{__TOKEN_SPECIFICATION["NUMBER_NEGATIVE_OPT"]})'
                      f'(?:{__TOKEN_SPECIFICATION["MULTIPLICATION"]}|{__TOKEN_SPECIFICATION["DIVISION"]})'
                      f'(?P<SECOND_NUMBER>{__TOKEN_SPECIFICATION["NUMBER_NEGATIVE_OPT"]})',
                      expression)

    if token:
        if token.group("MULTIPLICATION"):
            result = float(token.group("FIRST_NUMBER")) * float(token.group("SECOND_NUMBER"))
        else:
            result = float(token.group("FIRST_NUMBER")) / float(token.group("SECOND_NUMBER"))

        return re.sub(token.re, str(result), expression, 1)

    return None

def __handle_addition_subtraction(expression: str) -> str:
    token = re.search(f'(?P<FIRST_NUMBER>{__TOKEN_SPECIFICATION["NUMBER_NEGATIVE_OPT"]})'
                      f'(?:{__TOKEN_SPECIFICATION["ADDITION"]}|{__TOKEN_SPECIFICATION["SUBTRACTION"]})'
                      f'(?P<SECOND_NUMBER>{__TOKEN_SPECIFICATION["NUMBER_NEGATIVE_OPT"]})',
                      expression)

    if token:
        if token.group("ADDITION"):
            result = float(token.group("FIRST_NUMBER")) + float(token.group("SECOND_NUMBER"))
        else:
            result = float(token.group("FIRST_NUMBER")) - float(token.group("SECOND_NUMBER"))

        return re.sub(token.re, str(result), expression, 1)

    return None


__OPERATION_HANDLERS = (
    __handle_parenthesis,
    __handle_factorial,
    __handle_negate,
    __handle_max_min_average,
    __handle_power,
    __handle_multiplication_division,
    __handle_addition_subtraction,
)

exp = "4 + (5 + 2! - 3!) + ((5 * 3) @ 13)" # 19
print(calculate(exp))

# tok = re.search('(-?\d+(?:\.\d+)?)(?P<MULT>\*)(-?\d+(?:\.\d+)?)', "5*2")
# print(tok.group('GE'))
