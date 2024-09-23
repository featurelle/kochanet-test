from unittest import mock

from django.test import TestCase
from django.utils import timezone
from datetime import date, datetime, timedelta

from rest_framework.exceptions import ValidationError

from .models import Patient, GenderChoices
from .serializers import PatientSerializer


class PatientModelTest(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            full_name="John Doe",
            gender=GenderChoices.MALE,
            birthdate=date(1990, 6, 15),
            phone="1234567890",
            address="Cn432423432"
        )

    def test_age_calculation(self):
        def test_against_date(year, month, day, expected_age):
            # Mock the specific "current" date and evaluate the age
            mock_current_date = datetime(year, month, day, 12, 0, 0)
            with mock.patch('django.utils.timezone.now', return_value=timezone.make_aware(mock_current_date)):
                self.assertEqual(self.patient.age, expected_age)

        test_against_date(2024, 6, 14, 33)
        test_against_date(2024, 6, 15, 34)
        test_against_date(2025, 1, 1, 34)
        test_against_date(2026, 1, 1, 35)


class PatientSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'full_name': 'John Doe',
            'gender': 'm',
            'birthdate': str(date.today() - timedelta(days=365 * 30)),  # 30 years old
            'phone': '1234567890',
            'address': 'ChIJN1t_tDeuEmsRUsoyG83frY4'  # Sample Google Place ID
        }

    def test_valid_data(self):
        data = self.valid_data.copy()
        serializer = PatientSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_full_name(self):
        data = self.valid_data.copy()
        data['full_name'] = 'John123'  # Invalid full name (contains numbers)
        serializer = PatientSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_birthdate_future(self):
        data = self.valid_data.copy()
        data['birthdate'] = (date.today() + timedelta(days=1)).isoformat()  # Birthdate in the future
        serializer = PatientSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_birthdate_ancient(self):
        data = self.valid_data.copy()
        data['birthdate'] = (date.today() - timedelta(days=365 * 150)).isoformat()  # More than 120 years old
        serializer = PatientSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_phone(self):
        data = self.valid_data.copy()
        data['phone'] = 'abc123'  # Invalid phone (contains letters)
        serializer = PatientSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_address(self):
        data = self.valid_data.copy()
        data['address'] = 'Invalid!ID@'  # Invalid address (contains special characters)
        serializer = PatientSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
