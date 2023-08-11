import json
import pytest

from django.test import RequestFactory
from django.urls import reverse

from v1.administration import views, models


class TestAdministrationViews:
    # pylint: disable=attribute-defined-outside-init
    def setup_method(self):
        self.factory = RequestFactory()

    @pytest.mark.django_db
    def test_new_action_log_happy_path(self):
        post_data = {
            'action': 'Test Action 123'
        }

        request = self.factory.post(
            reverse('action-log-new'),
            content_type='application/json',
            data=json.dumps(post_data)
        )

        response = views.new_action_log(request)
        assert response.status_code == 200

        all_logs = models.ActionLog.objects.all()
        assert len(all_logs) == 1
        assert all_logs.first().action == 'Test Action 123'

    @pytest.mark.django_db
    def test_new_action_log_no_key(self):
        post_data = {
            'notaction': 'Test Action 123'
        }

        request = self.factory.post(
            reverse('action-log-new'),
            content_type='application/json',
            data=json.dumps(post_data)
        )

        response = views.new_action_log(request)
        assert response.status_code == 400

        all_logs = models.ActionLog.objects.all()
        assert len(all_logs) == 0

    @pytest.mark.django_db
    def test_new_action_log_too_long(self):
        post_data = {
            'action': '12345678901234567890123456789012345678901234567890'
                      '12345678901234567890123456789012345678901234567890'
                      '12345678901234567890123456789012345678901234567890'
                      '12345678901234567890123456789012345678901234567890'
                      '12345678901234567890123456789012345678901234567890'
                      '12345678901234567890123456789012345678901234567890'
        }

        request = self.factory.post(
            reverse('action-log-new'),
            content_type='application/json',
            data=json.dumps(post_data)
        )

        response = views.new_action_log(request)
        assert response.status_code == 400

        all_logs = models.ActionLog.objects.all()
        assert len(all_logs) == 0

    @pytest.mark.django_db
    def test_get_action_log_happy_path(self):
        models.ActionLog(action='Test 1').save()
        models.ActionLog(action='Test 2').save()
        models.ActionLog(action='Test 3').save()

        request = self.factory.get(
            reverse('action-log-all'),
            {
                'page': 0,
                'items': 3
            }
        )

        response = views.get_action_logs(request)
        assert response.status_code == 200

        content = json.loads(response.content)
        assert content['page'] == 0
        assert content['has_next_page'] is False
        assert content['has_prev_page'] is False
        assert len(content['actions']) == 3

    def test_get_action_log_no_items(self):
        request = self.factory.get(
            reverse('action-log-all'),
            {
                'page': 0,
                'items': 0
            }
        )

        response = views.get_action_logs(request)
        assert response.status_code == 400

    def test_get_action_log_negative_page(self):
        request = self.factory.get(
            reverse('action-log-all'),
            {
                'page': -1,
                'items': 3
            }
        )

        response = views.get_action_logs(request)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_get_mavp_happy_path(self):
        models.MAVP(
            facility_long='Indianapolis ARTCC',
            facility_short='ZID'
        ).save()
        models.MAVP(
            facility_long='Academy ARTCC',
            facility_short='ZAB'
        ).save()

        request = self.factory.get(
            reverse('mavp-all')
        )

        response = views.get_mavp(request)
        assert response.status_code == 200

        content = json.loads(response.content)
        assert len(content['mavp']) == 2
        assert content['mavp'][0]['facility_short'] in ['ZAB', 'ZID']

    @pytest.mark.django_db
    def test_new_mavp_happy_path(self):
        post_data = {
            'facility_short': 'ZAB',
            'facility_long': 'Academy ARTCC'
        }

        request = self.factory.post(
            reverse('mavp-new'),
            content_type='application/json',
            data=json.dumps(post_data)
        )

        response = views.new_mavp(request)
        assert response.status_code == 200

        all_mavps = models.MAVP.objects.all()
        assert len(all_mavps) == 1

        mavp = all_mavps.first()
        assert mavp.facility_short == 'ZAB'
        assert mavp.facility_long == 'Academy ARTCC'

    def test_new_mavp_no_short(self):
        post_data = {
            'wrong_facility_short': 'ZAB',
            'facility_long': 'Academy ARTCC'
        }

        request = self.factory.post(
            reverse('mavp-new'),
            content_type='application/json',
            data=json.dumps(post_data)
        )

        response = views.new_mavp(request)
        assert response.status_code == 400

    def test_new_mavp_no_long(self):
        post_data = {
            'facility_short': 'ZAB',
            'wrong_facility_long': 'Academy ARTCC'
        }

        request = self.factory.post(
            reverse('mavp-new'),
            content_type='application/json',
            data=json.dumps(post_data)
        )

        response = views.new_mavp(request)
        assert response.status_code == 400

    def test_new_mavp_short_too_long(self):
        post_data = {
            'facility_short': 'KZAB',
            'facility_long': 'Academy ARTCC'
        }

        request = self.factory.post(
            reverse('mavp-new'),
            content_type='application/json',
            data=json.dumps(post_data)
        )

        response = views.new_mavp(request)
        assert response.status_code == 400

    def test_new_mavp_long_too_long(self):
        post_data = {
            'facility_short': 'ZAB',
            'facility_long': '12345678901234567890123456789012345678901234567890'
                             '12345678901234567890123456789012345678901234567890'
                             '12345678901234567890123456789012345678901234567890'
                             '12345678901234567890123456789012345678901234567890'
                             '12345678901234567890123456789012345678901234567890'
                             '12345678901234567890123456789012345678901234567890'
        }

        request = self.factory.post(
            reverse('mavp-new'),
            content_type='application/json',
            data=json.dumps(post_data)
        )

        response = views.new_mavp(request)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_new_mavp_already_exists(self):
        models.MAVP(
            facility_short='ZAB',
            facility_long='Academy ARTCC'
        ).save()

        post_data = {
            'facility_short': 'ZAB',
            'facility_long': 'Academy ARTCC'
        }

        request = self.factory.post(
            reverse('mavp-new'),
            content_type='application/json',
            data=json.dumps(post_data)
        )

        response = views.new_mavp(request)
        assert response.status_code == 409

    @pytest.mark.django_db
    def test_delete_mavp_happy_path(self):
        models.MAVP(
            facility_short='ZAB',
            facility_long='Academy ARTCC'
        ).save()

        del_data = {
            'facility_short': 'ZAB'
        }

        request = self.factory.delete(
            reverse('mavp-delete'),
            content_type='application/json',
            data=json.dumps(del_data)
        )

        response = views.delete_mavp(request)
        assert response.status_code == 200
        assert len(models.MAVP.objects.all()) == 0

    def test_delete_mavp_no_short(self):
        del_data = {
            'facility_long': 'Academy ARTCC'
        }

        request = self.factory.delete(
            reverse('mavp-delete'),
            content_type='application/json',
            data=json.dumps(del_data)
        )

        response = views.delete_mavp(request)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_delete_mavp_does_not_exist(self):
        del_data = {
            'facility_short': 'ZAB'
        }

        request = self.factory.delete(
            reverse('mavp-delete'),
            content_type='application/json',
            data=json.dumps(del_data)
        )

        response = views.delete_mavp(request)
        assert response.status_code == 404
