import re
import math
from statistics import mean


_NUMBER_REGEX = r'\d+(?:\.\d+)?'
_NEGATIVE_NUMBER_REGEX = f'-?{_NUMBER_REGEX}'
_LEFT_PARENTHESIS_REGEX = r'(?:\()'
_RIGHT_PARENTHESIS_REGEX = r'(?:\))'


def calculate(expression: str) -> str:
    if type(expression) is not str:
        raise TypeError("Expression input should be of str type.")

    return _calculate(expression.replace(" ", ""))

def _calculate(expression: str) -> str:
    if _is_end_of_calculation(expression):
        return expression

    for regex, handler in _TOKEN_SPECIFICATION.items():
        match = re.search(regex, expression)
        if match:
            operands = match.groups()
            step_result = str(handler(*operands))
            solved_step_expression = re.sub(match.re, step_result, expression, count=1)
            return _calculate(solved_step_expression)

    raise ValueError(f'Expression: {expression} is not legal!')

def _generate_expression_regex(operation: str, is_single_variable: bool = False, is_negative_legal: bool = True) -> str:
    number_regex = f'({_NEGATIVE_NUMBER_REGEX})' if is_negative_legal else f'({_NUMBER_REGEX})'
    return f'{number_regex}{operation}' if is_single_variable else f'{number_regex}{operation}{number_regex}'

def _is_end_of_calculation(expression: str) -> bool:
    return re.fullmatch(f'{_NEGATIVE_NUMBER_REGEX}', expression) is not None


_TOKEN_SPECIFICATION = {
    f'{_LEFT_PARENTHESIS_REGEX}([^{_LEFT_PARENTHESIS_REGEX}{_RIGHT_PARENTHESIS_REGEX}]*){_RIGHT_PARENTHESIS_REGEX}':
        lambda x: _calculate(x),
    _generate_expression_regex(r'(?:!)', True, False): lambda x: math.factorial(int(x)),
    _generate_expression_regex(r'(?:~)', True): lambda x: -1 * float(x),
    _generate_expression_regex(r'(?:@)'): lambda x, y: mean([float(x), float(y)]),
    _generate_expression_regex(r'(?:\&)'): lambda x, y: min(float(x), float(y)),
    _generate_expression_regex(r'(?:\$)'): lambda x, y: max(float(x), float(y)),
    _generate_expression_regex(r'(?:\^)'): lambda x, y: float(x) ** float(y),
    _generate_expression_regex(r'(?:\*)'): lambda x, y: float(x) * float(y),
    _generate_expression_regex(r'(?:/)'): lambda x, y: float(x) / float(y),
    _generate_expression_regex(r'(?:\+)'): lambda x, y: float(x) + float(y),
    _generate_expression_regex(r'(?:-)'): lambda x, y: float(x) - float(y),
}