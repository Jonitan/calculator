import re

__token_specification = [
    ('ADDITION', r'\+'),
    ('SUBTRACTION', r'-'),
    ('MULTIPLICATION', r'\*'),
    ('DIVISION', r'/'),
    ('POWER', r'\^'),
    ('NEGATE', r'~'),
    ('MODULE', r'%'),
    ('FACTORIAL', r'!'),
    ('AVERAGE', r'@'),
    ('MAX', r'\$'),
    ('MIN', r'&'),
    ('LEFT_PARENTHESIS', r'\('),
    ('RIGHT_PARENTHESIS', r'\)'),
    ('NUMBER', r'\w+')
]

__tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in __token_specification)


def calculate(expression=str):
    if type(expression) is not str:
        raise TypeError("Expression input should be of str type.")

    expression = __remove_spaces(expression)

    return __calculate(expression)


def __calculate(expression):
    token = re.search(__tok_regex, expression)

    if token is None:
        return 0
    else:
        result = __token_to_operation(token.lastgroup)
        return result + __calculate(expression[token.end()::])


def __token_to_operation(argument):
    return __token_switcher[argument]()


def __remove_spaces(expression):
    return re.sub("\s", "", expression)


def __zero():
    return 1


__token_switcher = {
    'ADDITION': __zero,
    'SUBTRACTION': __zero,
    'MULTIPLICATION': __zero,
    'DIVISION': __zero,
    'POWER': __zero,
    'NEGATE': __zero,
    'MODULE': __zero,
    'FACTORIAL': __zero,
    'AVERAGE': __zero,
    'MAX': __zero,
    'MIN': __zero,
    'LEFT_PARENTHESIS': __zero,
    'RIGHT_PARENTHESIS': __zero,
    'NUMBER': __zero,
}

exp = "523 + 3 * 7 - (24 + ((5 - 3) + 2)) + 52 + (7 - 3)"
print(calculate(exp))

# x = calc.open_parenthesis(exp)
# print(x.string)
# print(x.span())
# print(x.group())


# @classmethod
# def open_parenthesis(cls, expression):
#     left_par_splited = re.split(r'\(', expression)
#     left_par_splited = list(filter(None, left_par_splited))
#     par_splited = list(re.split(r'\)', item) for item in left_par_splited)
#     par_splited = list(list(filter(None, item)) for item in par_splited)
#     # par_splited = list(filter(None, par_splited))
#     print(par_splited)
#         # TODO: Calc expression.
