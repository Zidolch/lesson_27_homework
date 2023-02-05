
from rest_framework import serializers


def check_is_published(value: bool):
    if value:
        raise serializers.ValidationError('Недопустимый статус публикации.')
