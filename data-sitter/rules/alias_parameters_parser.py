from typing import Callable
from parse import with_pattern, Parser

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


def parse_array_of(type_name: str, type_parser: Callable):
    items_type = TypeBuilder.with_many0(type_parser, type_parser.pattern, listsep=",")
    _parser = Parser(f"{{value:{type_name}}}", extra_types={type_name: items_type})

    def parse_list(text: str):
        text_without_brackets = text[1:-1]
        cosa = _parser.parse(text_without_brackets)
        return cosa['value']

    list_pattern = rf"\[{items_type.pattern}\]"
    return with_pattern(list_pattern)(parse_list)


# parse_variant = TypeBuilder.make_variant([parse_number, parse_color])


alias_parameters_types = {
    "Integer": parse_int,
    "Integers": parse_array_of("Integer", parse_int),
    "Float": parse_float,
    "Floats": parse_array_of("Float", parse_float),
    "Number": parse_number,
    "Numbers": parse_array_of("Number", parse_number),
    "String": parse_string,
    "Strings": parse_array_of("String", parse_string),
}
