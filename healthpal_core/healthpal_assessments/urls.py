from django.urls import path
from .views import PatientAssessmentListCreateView, PatientAssessmentRetrieveUpdateDestroyView

urlpatterns = [
    path('', PatientAssessmentListCreateView.as_view(), name='assessment-list-create'),
    path('<int:pk>/', PatientAssessmentRetrieveUpdateDestroyView.as_view(), name='assessment-detail'),
]
