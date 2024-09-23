from django.core.validators import MaxValueValidator
from django.utils import timezone


def get_date_not_future_validator(message) -> MaxValueValidator:
    return MaxValueValidator(
        limit_value=timezone.now().date(),
        message=message
    )
