from typing import Callable
from parse import with_pattern, Parser

from parse_type import TypeBuilder


class NotCompatibleTypes(Exception):
    pass


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
        validation = _parser.parse(text_without_brackets)
        if validation is None:
            raise NotCompatibleTypes(f"This shouldn't happens but items of the array '{type_name}' are not compatible?.")

        return validation['value']

    list_pattern = rf"\[{items_type.pattern}\]"
    return with_pattern(list_pattern)(parse_list)


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







# class Store()
#     pass


# values = {"classes": ["UNCLASSIFIED"], "min_length": 5, "max_length": 50}


# alias_parser = Parser("Value in {possible_values:Strings}", extra_types=alias_parameters_types)
# # print(alias_parser.parse("Value In ['UNCLASSIFIED', 'CLASSIFIED']"))

# with Store(values=values) as store:
#     print(alias_parser.parse("Value In $values.classes"))
#     print(store.)
