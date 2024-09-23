from unittest import mock

from django.test import TestCase
from django.utils import timezone
from datetime import date, datetime, timedelta

from rest_framework.exceptions import ValidationError

from healthpal_shared.tests import BaseSerializerTestCase
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


class PatientSerializerTest(BaseSerializerTestCase):

    serializer_class = PatientSerializer

    def setUp(self):
        self.valid_data = {
            'full_name': 'John Doe',
            'gender': 'm',
            'birthdate': str(date.today() - timedelta(days=365 * 30)),  # 30 years old
            'phone': '1234567890',
            'address': 'ChIJN1t_tDeuEmsRUsoyG83frY4'  # Sample Google Place ID
        }

    def test_valid_data(self):
        self._test_valid_data()

    def test_invalid_full_name(self):
        invalid_full_name_format = 'John123'

        self._test_invalid_data_part({'full_name': invalid_full_name_format})

    def test_invalid_birthdate(self):
        invalid_birthdate_future = (date.today() + timedelta(days=1)).isoformat()
        invalid_birthdate_ancient = (date.today() - timedelta(days=365 * 150)).isoformat()

        key = 'birthdate'

        self._test_invalid_data_part({key: invalid_birthdate_future})
        self._test_invalid_data_part({key: invalid_birthdate_ancient})

    def test_invalid_phone(self):
        invalid_phone_format = 'abc123'

        self._test_invalid_data_part({'phone': invalid_phone_format})

    def test_invalid_address(self):
        invalid_address_format = 'Invalid!ID@'
        self._test_invalid_data_part({'address': invalid_address_format})
