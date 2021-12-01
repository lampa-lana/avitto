import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_date_edit(value):
    """
    проверка, что дата редактирования не позже текущей даты
    """
    if value.date() > datetime.datetime.now().date():
        raise ValidationError(
            'Указанная дата не может быть больше текущей даты')


def validate_birth_date(value):
    """
    Проверяет корректность даты рождения
    """
    if value >= (timezone.now() + datetime.timedelta(days=1)).date():
        raise ValidationError(
            'Указанная дата не может быть больше текущей даты', params={'value': value},)
