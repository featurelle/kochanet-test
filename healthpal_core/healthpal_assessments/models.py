from django.db import models

from healthpal_patients.models import Patient


class PatientAssessment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type = models.CharField()
    datetime = models.DateTimeField()
    score = models.PositiveSmallIntegerField()
    # qna_rounds m2o

    def __str__(self):
        return f'Assessment {self.pk} ({self.patient.full_name}, {self.datetime})'


class AssessmentQnARound(models.Model):
    """Represents one Question-Answer round during the PatientAssessment"""
    patient_assessment = models.ForeignKey(PatientAssessment, on_delete=models.CASCADE, related_name='qna_rounds')
    question = models.CharField(null=False)
    answer = models.CharField()

    def __str__(self):
        question = self.question
        question_short = question if len(question) <= 15 else question[:25] + '...'

        return (
            f'QnA Round {self.pk} '
            f'('
            f'Assessment {self.patient_assessment.pk}, '
            f'{self.patient_assessment.patient.full_name}, '
            f'"{question_short}"'
            f')'
        )   # e.g. QnA Round 1, (Assessment 1, John Doe, "So how are feeling, Joh...")
