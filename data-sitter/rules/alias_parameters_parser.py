from parse import with_pattern

from parse_type import TypeBuilder


@with_pattern(r"-?\d+")
def parse_int(text):
    return int(text)


@with_pattern(r"-?\d*.\d+")
def parse_float(text):
    return float(text)


@with_pattern(r"-?\d+.?\d*")
def parse_number(text):
    if "." in text:
        return float(text)
    return int(text)


@with_pattern(r"|".join([r'"[^"]*"', "'[^']*'"]))
def parse_string(text: str):
    return text[1:-1]


def parse_array_of(type_parser: callable):
    @with_pattern(r"\[[^\]]*\]")
    def parser(text):
        return TypeBuilder.with_many0(type_parser, listsep=",")(text[1:-1])
    return parser


alias_parameters_types = {
    "Integer": parse_int,
    "Integers": parse_array_of(parse_int),
    "Float": parse_float,
    "Floats": parse_array_of(parse_float),
    "Number": parse_number,
    "Numbers": parse_array_of(parse_number),
    "String": parse_string,
    "Strings": parse_array_of(parse_string),
}
