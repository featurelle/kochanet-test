from django.db import models
from django.utils import timezone
from dateutils import relativedelta


class GenderChoices(models.TextChoices):
    MALE = 'm', 'male'
    FEMALE = 'f', 'female'


class Patient(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    gender = models.CharField(choices=GenderChoices.choices)
    birthdate = models.DateField()  # Todo: not in the future
    phone = models.CharField()
    address = models.CharField()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self):
        today = timezone.now().date()
        age = relativedelta(today, self.birthdate).years
        return age

    def __str__(self):
        return f'Patient {self.pk} ({self.full_name})'
