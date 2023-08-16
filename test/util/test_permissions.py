from datetime import datetime
from unittest import TestCase
import pytest
from rest_framework.test import APIRequestFactory
from rest_framework_api_key.models import APIKey
from util.permissions import HasAPIKeyOrReadOnly


class TestPermissions(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_has_permission_safe_method(self):
        request = self.factory.get(
            '/test-method'
        )

        self.assertTrue(HasAPIKeyOrReadOnly().has_permission(request, None))

    @pytest.mark.django_db
    def test_has_permission_valid_key(self):
        _, key = APIKey.objects.create_key(name='test')
        request = self.factory.post(
            '/test-method',
            HTTP_AUTHORIZATION=f'Api-Key {key}'
        )

        self.assertTrue(HasAPIKeyOrReadOnly().has_permission(request, None))

    def test_has_permission_no_authorization(self):
        request = self.factory.post(
            '/test-method'
        )

        self.assertFalse(HasAPIKeyOrReadOnly().has_permission(request, None))

    @pytest.mark.django_db
    def test_has_permission_bad_format(self):
        _, key = APIKey.objects.create_key(name='test')
        request = self.factory.post(
            '/test-method',
            HTTP_AUTHORIZATION=f'BadFormatApiKey{key}'
        )

        self.assertFalse(HasAPIKeyOrReadOnly().has_permission(request, None))

    @pytest.mark.django_db
    def test_has_permission_key_does_not_exist(self):
        request = self.factory.post(
            '/test-method',
            HTTP_AUTHORIZATION='Api-Key thiskeydoesnotexist'
        )

        self.assertFalse(HasAPIKeyOrReadOnly().has_permission(request, None))

    @pytest.mark.django_db
    def test_has_permission_key_expired(self):
        expiry_date = datetime(year=2000, month=1, day=1)
        _, key = APIKey.objects.create_key(
            name='test',
            expiry_date=expiry_date
        )

        request = self.factory.post(
            '/test-method',
            HTTP_AUTHORIZATION=f'Api-Key {key}'
        )

        self.assertFalse(HasAPIKeyOrReadOnly().has_permission(request, None))

    @pytest.mark.django_db
    def test_has_permission_key_revoked(self):
        _, key = APIKey.objects.create_key(
            name='test',
            revoked=True
        )

        request = self.factory.post(
            'test-method',
            HTTP_AUTHORIZATION=f'Api-Key {key}'
        )

        self.assertFalse(HasAPIKeyOrReadOnly().has_permission(request, None))
