from django.db import models


class GenderChoices(models.TextChoices):
    MALE = 'm', 'male'
    FEMALE = 'f', 'female'


class Patient(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    gender = models.CharField(choices=GenderChoices.choices)
    phone = models.CharField()
    address = models.CharField()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'Patient {self.pk} ({self.full_name})'
