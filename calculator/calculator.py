import re
import math
from typing import Union
from statistics import mean


_NUMBER_REGEX = r'\d+(?:\.\d+)?'
_NUMBER_NEGATIVE_OPT_REGEX = r'-?\d+(?:\.\d+)?'

OPERATION_REGEX_INDEX = 0
OPERATION_HANDLER_INDEX = 1


def calculate(expression: str) -> Union[int, float]:
    if type(expression) is not str:
        raise TypeError("Expression input should be of str type.")

    return _calculate(expression.replace(" ", ""))

def _calculate(expression: str) -> Union[int, float]:
    if _is_end_of_calculation(expression):
        return expression

    for _, value in _TOKEN_SPECIFICATION.items():
        tmp_result = _handle(expression, value)
        if tmp_result is not None:
            return _calculate(tmp_result)

    raise ValueError(f'Expression: {expression} is not legal!')

def _one_variable_operation(operation: str, is_negative_legal: bool = False) -> str:
    if is_negative_legal is False:
        return f'(?P<NUMBER>{_NUMBER_REGEX}){operation}'
    else:
        return f'(?P<NUMBER>{_NUMBER_NEGATIVE_OPT_REGEX}){operation}'

def _two_variable_operation(operation: str, is_negative_legal: bool = False) -> str:
    if is_negative_legal is False:
        return f'(?P<FIRST_NUMBER>{_NUMBER_REGEX}){operation}' \
               f'(?P<SECOND_NUMBER>{_NUMBER_REGEX})'
    else:
        return f'(?P<FIRST_NUMBER>{_NUMBER_NEGATIVE_OPT_REGEX}){operation}' \
               f'(?P<SECOND_NUMBER>{_NUMBER_NEGATIVE_OPT_REGEX})'

def _is_end_of_calculation(expression: str) -> bool:
    return re.fullmatch(f'{_NUMBER_NEGATIVE_OPT_REGEX}', expression) is not None

def _handle(expression: str, operation_details) -> str:
    token = re.search(operation_details[OPERATION_REGEX_INDEX], expression)
    if token:
        return re.sub(token.re, operation_details[OPERATION_HANDLER_INDEX](token), expression, 1)

def _handle_parenthesis(token) -> str:
    return str(_calculate(token.group("EXTRACTED_EXPRESSION")))

def _handle_factorial(token) -> str:
    return str(math.factorial(float(token.group("NUMBER"))))

def _handle_negate(token) -> str:
    return str(-1 * float(token.group("NUMBER")))

def _handle_max_min_average(token) -> str:
    if token.group("MAX"):
        return str(max(float(token.group("FIRST_NUMBER")), float(token.group("SECOND_NUMBER"))))
    elif token.group("MIN"):
        return str(min(float(token.group("FIRST_NUMBER")), float(token.group("SECOND_NUMBER"))))
    else:
        return str(mean([float(token.group("FIRST_NUMBER")), float(token.group("SECOND_NUMBER"))]))

def _handle_power(token) -> str:
    return str(float(token.group("FIRST_NUMBER")) ** float(token.group("SECOND_NUMBER")))

def _handle_multiplication_division(token) -> str:
    if token.group("MULTIPLICATION"):
        return str(float(token.group("FIRST_NUMBER")) * float(token.group("SECOND_NUMBER")))
    else:
        return str(float(token.group("FIRST_NUMBER")) / float(token.group("SECOND_NUMBER")))

def _handle_addition_subtraction(token) -> str:
    if token.group("ADDITION"):
        return str(float(token.group("FIRST_NUMBER")) + float(token.group("SECOND_NUMBER")))
    else:
        return str(float(token.group("FIRST_NUMBER")) - float(token.group("SECOND_NUMBER")))


_LEFT_PARENTHESIS_REGEX = r'(?P<LEFT_PARENTHESIS>\()'
_RIGHT_PARENTHESIS_REGEX = r'(?P<RIGHT_PARENTHESIS>\))'
_FACTORIAL_REGEX = r'(?P<FACTORIAL>!)'
_NEGATE_REGEX = r'(?P<NEGATE>~)'
_AVERAGE_REGEX = r'(?P<AVERAGE>@)'
_MIN_REGEX = r'(?P<MIN>\&)'
_MAX_REGEX = r'(?P<MAX>\$)'
_POWER_REGEX = r'(?P<POWER>\^)'
_MULTIPLICATION_REGEX = r'(?P<MULTIPLICATION>\*)'
_DIVISION_REGEX = r'(?P<DIVISION>/)'
_ADDITION_REGEX = r'(?P<ADDITION>\+)'
_SUBTRACTION_REGEX = r'(?P<SUBTRACTION>-)'

_TOKEN_SPECIFICATION = {
    'PARENTHESIS_PAIR': (f'{_LEFT_PARENTHESIS_REGEX}'
                         f'(?P<EXTRACTED_EXPRESSION>[^{_LEFT_PARENTHESIS_REGEX}{_RIGHT_PARENTHESIS_REGEX}]*)'
                         f'{_RIGHT_PARENTHESIS_REGEX}', _handle_parenthesis),
    'FACTORIAL': (_one_variable_operation(f'{_FACTORIAL_REGEX}', False), _handle_factorial),
    'NEGATE': (_one_variable_operation(f'{_NEGATE_REGEX}', True), _handle_negate),
    'AVERAGE_MAX_MIN': (_two_variable_operation(f'(?:{_AVERAGE_REGEX}|{_MIN_REGEX}|{_MAX_REGEX})', True),
                        _handle_max_min_average),
    'POWER': (_two_variable_operation(f'{_POWER_REGEX}', True), _handle_power),
    'MULTIPLICATION_DIVISION': (_two_variable_operation(f'(?:{_MULTIPLICATION_REGEX}|{_DIVISION_REGEX})', True),
                                _handle_multiplication_division),
    'ADDITION_SUBTRACTION': (_two_variable_operation(f'(?:{_ADDITION_REGEX}|{_SUBTRACTION_REGEX})', True),
                             _handle_addition_subtraction),
}

exp = "4 + ((((5 + 2! - 3!)))) + ((5 * 3) @ 13)" # 19
print(calculate(exp))