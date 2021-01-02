import re
import math
from typing import Union
from statistics import mean


_NUMBER_REGEX = r'\d+(?:\.\d+)?'
_NUMBER_NEGATIVE_OPT_REGEX = f'-?{_NUMBER_REGEX}'
_LEFT_PARENTHESIS_REGEX = r'(?:\()'
_RIGHT_PARENTHESIS_REGEX = r'(?:\))'


def calculate(expression: str) -> Union[int, float]:
    if type(expression) is not str:
        raise TypeError("Expression input should be of str type.")

    return _calculate(expression.replace(" ", ""))

def _calculate(expression: str) -> Union[int, float]:
    if _is_end_of_calculation(expression):
        return expression

    for regex, handler in _TOKEN_SPECIFICATION.items():
        match = re.search(regex, expression)
        if match:
            solved_step_expression = re.sub(match.re, str(handler(*match.groups())), expression, 1)
            return _calculate(solved_step_expression)

    raise ValueError(f'Expression: {expression} is not legal!')

def _add_operation_variables(operation: str, is_single_variable: bool = False, is_negative_legal: bool = False) -> str:
    number_regex = _NUMBER_NEGATIVE_OPT_REGEX if is_negative_legal else _NUMBER_REGEX
    return f'(?P<NUMBER>{number_regex}){operation}' if is_single_variable else f'(?P<FIRST_NUMBER>{number_regex})' \
                                                                               f'{operation}' \
                                                                               f'(?P<SECOND_NUMBER>{number_regex})'

def _is_end_of_calculation(expression: str) -> bool:
    return re.fullmatch(f'{_NUMBER_NEGATIVE_OPT_REGEX}', expression) is not None


_TOKEN_SPECIFICATION = {
    f'{_LEFT_PARENTHESIS_REGEX}(?P<EXTRACTED_EXPRESSION>[^{_LEFT_PARENTHESIS_REGEX}{_RIGHT_PARENTHESIS_REGEX}]*)'
    f'{_RIGHT_PARENTHESIS_REGEX}': lambda x: _calculate(x),
    _add_operation_variables(r'(?:!)', True, False): lambda x: math.factorial(float(x)),
    _add_operation_variables(r'(?:~)', True, True): lambda x: -1 * float(x),
    _add_operation_variables(r'(?:@)', False, True): lambda x, y: mean([float(x), float(y)]),
    _add_operation_variables(r'(?:\&)', False, True): lambda x, y: min(float(x), float(y)),
    _add_operation_variables(r'(?:\$)', False, True): lambda x, y: max(float(x), float(y)),
    _add_operation_variables(r'(?:\^)', False, True): lambda x, y: float(x) ** float(y),
    _add_operation_variables(r'(?:\*)', False, True): lambda x, y: float(x) * float(y),
    _add_operation_variables(r'(?:/)', False, True): lambda x, y: float(x) / float(y),
    _add_operation_variables(r'(?:\+)', False, True): lambda x, y: float(x) + float(y),
    _add_operation_variables(r'(?:-)', False, True): lambda x, y: float(x) - float(y),
}

exp = "4 + ((((5 + 2! - 3!)))) + ((5 * 3) @ 13)" # 19
print(calculate(exp))