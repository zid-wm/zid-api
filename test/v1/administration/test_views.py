import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from v1.administration import models


class TestActionLogViews(APITestCase):
    @pytest.mark.django_db
    def test_action_log_get(self):
        models.ActionLog(action='Test Action 1').save()
        models.ActionLog(action='Test Action 2').save()
        models.ActionLog(action='Test Action 3').save()

        url = reverse('action-log')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(3, len(content))
        self.assertEqual(content[0]['action'], 'Test Action 3')

    @pytest.mark.django_db
    def test_action_log_post(self):
        url = reverse('action-log')
        data = {
            'action': 'Test Action'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        content = response.json()
        self.assertIn('action', content)
        self.assertIn('timestamp', content)
        self.assertEqual(content['action'], 'Test Action')


class TestMAVPViews(APITestCase):
    @pytest.mark.django_db
    def test_mavp_get(self):
        models.MAVP(
            facility_short='ZTA',
            facility_long='Test ARTCC'
        ).save()
        models.MAVP(
            facility_short='ZAB',
            facility_long='Academy ARTCC'
        ).save()

        url = reverse('mavp')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()
        self.assertIn('ZTA', [item['facility_short'] for item in content])
        self.assertIn('ZAB', [item['facility_short'] for item in content])

    @pytest.mark.django_db
    def test_mavp_post(self):
        url = reverse('mavp')
        data = {
            'facility_short': 'ZAB',
            'facility_long': 'Academy ARTCC'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        content = response.json()
        self.assertEqual(content['facility_short'], 'ZAB')
        self.assertEqual(content['facility_long'], 'Academy ARTCC')

    @pytest.mark.django_db
    def test_mavp_post_already_exists(self):
        models.MAVP(
            facility_short='ZAB',
            facility_long='Academy ARTCC'
        ).save()

        url = reverse('mavp')
        data = {
            'facility_short': 'ZAB',
            'facility_long': 'Academy ARTCC'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = response.json()
        self.assertEqual(
            content['facility_short'][0],
            'mavp with this facility short already exists.'
        )

    @pytest.mark.django_db
    def test_mavp_delete(self):
        models.MAVP(
            facility_short='ZAB',
            facility_long='Academy ARTCC'
        ).save()

        url = reverse('mavp-delete', kwargs={
            'pk': 'ZAB'
        })
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        queryset = models.MAVP.objects.all()
        self.assertEqual(len(queryset), 0)

    @pytest.mark.django_db
    def test_mavp_delete_does_not_exist(self):
        url = reverse('mavp-delete', kwargs={
            'pk': 'ZAB'
        })
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        content = response.json()
        self.assertEqual(content['detail'], 'Not found.')
