from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from healthpal_patients.models import Patient
from healthpal_util.validators import get_date_not_future_validator


# Validators
type_regex_validator = RegexValidator(
    regex=r"^[A-Za-z0-9]+([ -][A-Za-z0-9]+)*$",
    message="Invalid type format. Use letters, numbers, spaces, or hyphens. Start and end with letters or numbers."
)

score_max_validator = MaxValueValidator(
    limit_value=100,
    message="Score cannot be greater than 100."
)

date_not_future_max_validator = get_date_not_future_validator(
    message="Assessment date cannot be in the future."
)


# Since validator can't access other fields, we need to define a function that'll also be used in a serializer
def validate_assessment_date_gte_patients_birthdate(assessment_date: date, patient_birthdate: date):
    if assessment_date < patient_birthdate:
        raise ValidationError("Assessment date cannot be before the patient's birthdate.")


# Models
class PatientAssessment(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )
    type = models.CharField(
        validators=[type_regex_validator],
        max_length=64
    )
    date = models.DateField(
        validators=[date_not_future_max_validator],
        default=timezone.now
    )
    score = models.PositiveSmallIntegerField(
        validators=[score_max_validator]
    )

    # Related fields:
    # qna_rounds (m2o)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'date', 'type'],
                name='unique_patient_date_type'
            ),
        ]

    def save(self, *args, **kwargs):
        # Validation in save method, since it cannot be done on the field-level
        # Since we only have one usage for now, I don't separate it in order not to create overhead
        validate_assessment_date_gte_patients_birthdate(self.date, self.patient.birthdate)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Assessment {self.pk} ({self.patient.full_name}, {self.date})'


class AssessmentQnARound(models.Model):
    """Represents one Question-Answer round during the PatientAssessment"""
    patient_assessment = models.ForeignKey(
        PatientAssessment,
        on_delete=models.CASCADE,
        related_name='qna_rounds'
    )
    # Since there's no way to guess qna format, neither validations nor max_length are applied for now
    question = models.CharField()
    answer = models.CharField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'patient_assessment'],
                name='unique_question_assessment'
            )
        ]

    def __str__(self):
        question = self.question
        question_short = question if len(question) <= 15 else question[:25] + '...'

        return (
            f'QnA Round {self.pk} ('
            f'Assessment {self.patient_assessment.pk}, '
            f'{self.patient_assessment.patient.full_name}, '
            f'"{question_short}")'
        )   # e.g. QnA Round 1, (Assessment 1, John Doe, "So how are feeling, Joh...")
