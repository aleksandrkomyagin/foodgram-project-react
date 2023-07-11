import re

from rest_framework import serializers


def validate_username(value):
    if value == 'me':
        raise serializers.ValidationError(
            'Нельзя использовать юзернэйм <me>.',
            {'value': value}
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        symbol = "".join(set(re.findall(r'[^a-zA-Z0-9-_\.+@]', value)))
        raise serializers.ValidationError(
            f'Не допустимые символы <{symbol}> в нике.'
        )
