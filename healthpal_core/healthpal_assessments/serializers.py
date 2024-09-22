from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework import serializers

from healthpal_patients.models import Patient
from .models import PatientAssessment, AssessmentQnARound, validate_assessment_date_gte_patients_birthdate


class QnARoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQnARound
        fields = ['question', 'answer']


class PatientAssessmentSerializer(serializers.ModelSerializer):
    qna_rounds = QnARoundSerializer(many=True, required=True)

    class Meta:
        model = PatientAssessment
        fields = '__all__'

    def validate_date(self, value):
        patient_id = self.get_initial().get('patient')

        if not patient_id or not isinstance(patient_id, int):
            return value  # Skip validation if no valid patient_id provided

        try:
            patient = Patient.objects.get(id=patient_id)
        except (Patient.DoesNotExist, ValueError):
            return value  # Skip validation if patient does not exist or ID is invalid

        # Perform validation for the assessment date being >= patient's birthdate
        try:
            validate_assessment_date_gte_patients_birthdate(value, patient.birthdate)
        except ModelValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def create(self, validated_data):
        qna_rounds_data = validated_data.pop('qna_rounds', [])

        # Create PatientAssessment
        patient_assessment = super().create(validated_data)

        # Handle AssessmentQnARounds creation if provided
        for qna_round_data in qna_rounds_data:
            AssessmentQnARound.objects.create(patient_assessment=patient_assessment, **qna_round_data)

        return patient_assessment

    def update(self, instance, validated_data):
        qna_rounds_data = validated_data.pop('qna_rounds', None)

        # Update PatientAssessment fields if provided
        super().update(instance, validated_data)

        # Handle AssessmentQnARounds updates if provided
        if qna_rounds_data is not None:
            instance.qna_rounds.all().delete()
            for qna_round_data in qna_rounds_data:
                AssessmentQnARound.objects.create(patient_assessment=instance, **qna_round_data)

        return instance
