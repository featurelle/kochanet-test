from unittest import mock

from django.test import TestCase
from django.utils import timezone
from datetime import date, datetime

from .models import Patient, GenderChoices


class PatientModelTest(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            gender=GenderChoices.MALE,
            birthdate=date(1990, 6, 15),
            phone="1234567890",
            address="123 Main St"
        )

    def test_age(self):
        """Test that the age is calculated correctly."""

        def test_against_date(year, month, day, expected_age):
            # Mock the specific "current" date and evaluate the age
            mock_current_date = datetime(year, month, day, 12, 0, 0)
            with mock.patch('django.utils.timezone.now', return_value=timezone.make_aware(mock_current_date)):
                self.assertEqual(self.patient.age, expected_age)

        test_against_date(2024, 6, 14, 33)
        test_against_date(2024, 6, 15, 34)
        test_against_date(2025, 1, 1, 34)
        test_against_date(2026, 1, 1, 35)
