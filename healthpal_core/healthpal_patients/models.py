from django.db import models


class GenderChoices(models.TextChoices):
    MALE = 'm', 'male'
    FEMALE = 'f', 'female'


class Patient(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    full_name = models.GeneratedField(
        expression=models.Func(
            models.F('first_name'),
            models.Value(' '),
            models.F('last_name'),
            function='CONCAT'
        ),
        editable=False,
        output_field=models.CharField()
    )
    gender = models.CharField(choices=GenderChoices.choices)
    phone = models.CharField()


    def __str__(self):
        return f'Patient {self.pk} ({self.full_name})'
