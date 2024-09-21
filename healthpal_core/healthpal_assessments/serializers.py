from rest_framework import serializers

from .models import PatientAssessment, AssessmentQnARound


class QnARoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQnARound
        fields = ['question', 'answer']


class PatientAssessmentSerializer(serializers.ModelSerializer):
    qna_rounds = QnARoundSerializer(many=True, required=False)

    class Meta:
        model = PatientAssessment
        fields = '__all__'

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
