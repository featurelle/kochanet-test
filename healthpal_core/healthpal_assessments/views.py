from rest_framework import generics
from .models import PatientAssessment
from .serializers import PatientAssessmentSerializer


class PatientAssessmentListCreateView(generics.ListCreateAPIView):
    queryset = PatientAssessment.objects.all()
    serializer_class = PatientAssessmentSerializer


class PatientAssessmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientAssessment.objects.all()
    serializer_class = PatientAssessmentSerializer
