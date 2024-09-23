from rest_framework import generics
from rest_framework.filters import OrderingFilter

from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

from healthpal_assessments.models import PatientAssessment
from healthpal_assessments.serializers import PatientAssessmentSerializer


# Utility classes
class PatientAssessmentFilter(filters.FilterSet):
    """
    Filtering class to filter PatientAssessments, usage in ListView:
        `filter_backends = (filters.DjangoFilterBackend, ...)`
        `filterset_class = PatientAssessmentFilter`
    """
    type = filters.CharFilter(field_name='type')
    date = filters.DateFilter(field_name='date')
    date_gte = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_lte = filters.DateFilter(field_name='date', lookup_expr='lte')
    patient = filters.NumberFilter(field_name='patient__id')

    class Meta:
        model = PatientAssessment
        fields = ['type', 'date', 'patient']


class SmallResultsSetPagination(PageNumberPagination):
    """Pagination class setup for page size from 5 up to 100"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserFilteredAccessMixin:
    serializer_class = PatientAssessmentSerializer

    def get_queryset(self):
        return PatientAssessment.objects.filter(patient__assigned_clinician=self.request.user)


# Views
class PatientAssessmentListCreateView(UserFilteredAccessMixin, generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = PatientAssessmentFilter
    pagination_class = SmallResultsSetPagination
    ordering_fields = ['date', 'type', 'patient']
    ordering = ['date']  # Default ordering


class PatientAssessmentRetrieveUpdateDestroyView(UserFilteredAccessMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
