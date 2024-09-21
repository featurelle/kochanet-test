from django.contrib import admin

from .models import PatientAssessment, AssessmentQnARound


@admin.register(PatientAssessment)
class PatientAssessmentAdmin(admin.ModelAdmin):
    pass


@admin.register(AssessmentQnARound)
class AssessmentQnARoundAdmin(admin.ModelAdmin):
    pass
