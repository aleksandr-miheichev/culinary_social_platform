from re import findall

from django.core.exceptions import ValidationError

ANTI_PATTERN = r'[^-a-zA-Z0-9_]+$'


def validate_slug(data):
    result = set(findall(ANTI_PATTERN, data))
    if result:
        raise ValidationError(
            f'В уникальном идентификаторе имеются недопустимые символы: '
            f'{"".join(result)}'
        )
    return data
