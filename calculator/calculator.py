import re
import math
from typing import Union
from statistics import mean


_NUMBER_REGEX = r'\d+(?:\.\d+)?'
_NUMBER_NEGATIVE_OPT_REGEX = f'-?{_NUMBER_REGEX}'
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


def calculate(expression: str) -> Union[int, float]:
    if type(expression) is not str:
        raise TypeError("Expression input should be of str type.")

    return _calculate(expression.replace(" ", ""))

def _calculate(expression: str) -> Union[int, float]:
    if _is_end_of_calculation(expression):
        return expression

    for regex, handler in _TOKEN_SPECIFICATION.items():
        tmp_result = _handle(expression, regex, handler)
        if tmp_result is not None:
            return _calculate(tmp_result)

    raise ValueError(f'Expression: {expression} is not legal!')

def _add_operation_variables(operation: str, is_single_variable: bool = False, is_negative_legal: bool = False) -> str:
    number_regex = _NUMBER_NEGATIVE_OPT_REGEX if is_negative_legal else _NUMBER_REGEX
    return f'(?P<NUMBER>{number_regex}){operation}' if is_single_variable else f'(?P<FIRST_NUMBER>{number_regex})' \
                                                                               f'{operation}' \
                                                                               f'(?P<SECOND_NUMBER>{number_regex})'

def _is_end_of_calculation(expression: str) -> bool:
    return re.fullmatch(f'{_NUMBER_NEGATIVE_OPT_REGEX}', expression) is not None

def _handle(expression: str, regex: str, handler) -> str:
    token = re.search(regex, expression)
    if token:
        return re.sub(token.re, handler(token), expression, 1)

def _handle_two_variable_operation(func):
    def _inner(token):
        return str(func(float(token.group("FIRST_NUMBER")), float(token.group("SECOND_NUMBER"))))
    return _inner

def _handle_single_variable_operation(func):
    def _inner(token):
        return str(func(float(token.group("NUMBER"))))
    return _inner

def _handle_parenthesis(token) -> str:
    return _calculate(token.group("EXTRACTED_EXPRESSION"))

@_handle_single_variable_operation
def _handle_factorial(a: float) -> float:
    return math.factorial(a)

@_handle_single_variable_operation
def _handle_negate(a: float) -> float:
    return -1 * a

@_handle_two_variable_operation
def _handle_average(a: float, b: float) -> float:
    return mean([a, b])

@_handle_two_variable_operation
def _handle_min(a: float, b: float) -> float:
    return min(a, b)

@_handle_two_variable_operation
def _handle_max(a: float, b: float) -> float:
    return max(a, b)

@_handle_two_variable_operation
def _handle_power(a: float, b: float) -> float:
    return a ** b

@_handle_two_variable_operation
def _handle_multiplication(a: float, b: float) -> float:
    return a * b

@_handle_two_variable_operation
def _handle_division(a: float, b: float) -> float:
    return a / b

@_handle_two_variable_operation
def _handle_addition(a: float, b: float) -> float:
    return a + b

@_handle_two_variable_operation
def _handle_subtraction(a: float, b: float) -> float:
    return a - b


_TOKEN_SPECIFICATION = {
    f'{_LEFT_PARENTHESIS_REGEX}(?P<EXTRACTED_EXPRESSION>[^{_LEFT_PARENTHESIS_REGEX}{_RIGHT_PARENTHESIS_REGEX}]*){_RIGHT_PARENTHESIS_REGEX}': _handle_parenthesis,
    _add_operation_variables(f'{_FACTORIAL_REGEX}', True, False): _handle_factorial,
    _add_operation_variables(f'{_NEGATE_REGEX}', True, True): _handle_negate,
    _add_operation_variables(f'{_AVERAGE_REGEX}', False, True): _handle_average,
    _add_operation_variables(f'{_MIN_REGEX}', False, True): _handle_min,
    _add_operation_variables(f'{_MAX_REGEX}', False, True): _handle_max,
    _add_operation_variables(f'{_POWER_REGEX}', False, True): _handle_power,
    _add_operation_variables(f'{_MULTIPLICATION_REGEX}', False, True): _handle_multiplication,
    _add_operation_variables(f'{_DIVISION_REGEX}', False, True): _handle_division,
    _add_operation_variables(f'{_ADDITION_REGEX}', False, True): _handle_addition,
    _add_operation_variables(f'{_SUBTRACTION_REGEX}', False, True): _handle_subtraction,
}

exp = "4 + ((((5 + 2! - 3!)))) + ((5 * 3) @ 13)" # 19
print(calculate(exp))