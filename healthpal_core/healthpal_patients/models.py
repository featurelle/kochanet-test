from datetime import date

from django.core.validators import RegexValidator, MinValueValidator, MinLengthValidator
from django.db import models
from django.utils import timezone
from dateutils import relativedelta

from healthpal_util.validators import get_date_not_future_validator


# Helper functions
def calculate_full_years_diff(date_from: date, date_to: date = None) -> int:
    """Calculate how many full years passed between date_from and date_to\n
    date_to defaults to today"""
    date_to = date_to or timezone.now().date()
    full_years_diff = relativedelta(date_to, date_from).years
    return full_years_diff


def calculate_age_threshold(years: int) -> date:
    """Calculate the date 'years' ago from today"""
    return timezone.now().date() - relativedelta(years=years)


# Choices
class GenderChoices(models.TextChoices):
    MALE = 'm', 'male'
    FEMALE = 'f', 'female'


# Validators
full_name_min_length_validator = MinLengthValidator(
    limit_value=2,
    message="Name should have at least 2 symbols."
)

full_name_regex_validator = RegexValidator(
    regex=r"^[A-Za-zÀ-ÿ]+([ '-][A-Za-zÀ-ÿ]+)*$",
    message="Invalid name format. Use letters, spaces, hyphens, or apostrophes. Start and end with letters."
)

phone_regex_validator = RegexValidator(
    regex=r"^[0-9]+$",
    message="Invalid phone format. Use digits only."
)

address_google_place_id_regex_validator = RegexValidator(
    regex=r"^[A-Za-z0-9_-]+$",
    message="Invalid Google Place ID format. Use digits, letters, underscores, or hyphens."
)

birthdate_not_future_max_validator = get_date_not_future_validator(
    message="Birthdate cannot be in the future."
)

def get_age_threshold() -> date:
    return calculate_age_threshold(120)

birthday_not_ancient_min_validator = MinValueValidator(
    limit_value=get_age_threshold,
    message="Birthdate cannot be more than 120 years ago."
)


# Model
class Patient(models.Model):
    full_name = models.CharField(
        validators=[full_name_min_length_validator, full_name_regex_validator],
        max_length=255
    )
    gender = models.CharField(
        choices=GenderChoices.choices,
        max_length=1
    )
    birthdate = models.DateField(
        validators=[birthdate_not_future_max_validator, birthday_not_ancient_min_validator]
    )
    phone = models.CharField(
        validators=[phone_regex_validator],
        max_length=15
    )
    address = models.CharField(
        validators=[address_google_place_id_regex_validator]
    )   # Assuming it's Google Places id, it can have any length

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['full_name', 'birthdate'],
                name='unique_name_birthdate'
            ),
        ]

    @property
    def age(self):
        return calculate_full_years_diff(self.birthdate)

    def __str__(self):
        return f'Patient {self.pk} ({self.full_name})'
