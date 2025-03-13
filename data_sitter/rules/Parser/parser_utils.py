import re


REF_PATTERN = r'\$values\.([a-zA-Z0-9_]+)'
VALUE_REF_PATTERN = re.compile(REF_PATTERN)


class MalformedReference(Exception):
    pass

class ReferenceNotFound(Exception):
    pass


def get_key_from_reference(reference: str):
    match = VALUE_REF_PATTERN.fullmatch(reference)
    if match is None:
        raise MalformedReference(f"Unrecognised Reference: {reference}")

    return match.group(1)


def get_value_from_reference(reference: str, values: dict):
    key = get_key_from_reference(reference)
    if key not in values:
        raise ReferenceNotFound(f"Reference '{key}' not found in values.")
    return values[key]
