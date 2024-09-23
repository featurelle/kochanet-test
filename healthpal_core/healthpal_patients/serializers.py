from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ['assigned_clinician']

    def create(self, validated_data):
        validated_data['assigned_clinician'] = self.context['request'].user
        return super().create(validated_data)
