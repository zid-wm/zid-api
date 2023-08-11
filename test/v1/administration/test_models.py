import pytest

from v1.administration.models import (
    ActionLog,
    MAVP
)


@pytest.mark.django_db
def test_action_log():
    ActionLog(action='Test Action 1').save()
    objects = ActionLog.objects.all()

    assert len(objects) == 1
    action_log = objects.first()
    assert action_log.action == 'Test Action 1'


@pytest.mark.django_db
def test_mavp():
    MAVP(
        facility_long='Academy ARTCC',
        facility_short='ZAB'
    ).save()
    objects = MAVP.objects.all()

    assert len(objects) == 1
    mavp = objects.first()
    assert mavp.facility_short == 'ZAB'
    assert mavp.facility_long == 'Academy ARTCC'
