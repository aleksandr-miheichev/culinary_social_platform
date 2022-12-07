from re import findall

from django.core.exceptions import ValidationError

ANTI_PATTERN = r'^[\w.@+-]+\z'


def validate_username(data):
    result = set(findall(ANTI_PATTERN, data))
    if result:
        raise ValidationError(
            f'В имени имеются недопустимые символы: {"".join(result)}'
        )
    return data
