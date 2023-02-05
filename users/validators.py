from datetime import date
from rest_framework import serializers
from dateutil.relativedelta import relativedelta


class IsAgeBigEnough:
    def __init__(self, min_age):
        self.min_age = min_age

    def __call__(self, value):
        if relativedelta(date.today(), value).years < self.min_age:
            raise serializers.ValidationError('Недопустимый возраст пользователя.')

