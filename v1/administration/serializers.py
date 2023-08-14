from rest_framework import serializers

from v1.administration import models


class ActionLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ActionLog
        fields = [
            'action',
            'timestamp'
        ]


class MAVPSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.MAVP
        fields = [
            'facility_short',
            'facility_long'
        ]
