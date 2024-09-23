from rest_framework import generics

from .models import Patient
from .serializers import PatientSerializer


# Utility class
class UserFilteredAccessMixin:
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(assigned_clinician=self.request.user)


# Views
class PatientListCreateView(UserFilteredAccessMixin, generics.ListCreateAPIView):
    pass


class PatientRetrieveUpdateDestroyView(UserFilteredAccessMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
