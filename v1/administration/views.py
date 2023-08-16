from rest_framework import generics
from rest_framework.schemas.openapi import AutoSchema
from rest_framework_api_key import permissions as api_key_permissions

from util.permissions import HasAPIKeyOrReadOnly
from v1.administration import models, serializers


class ActionLogView(generics.ListCreateAPIView):
    schema = AutoSchema(tags=['Administration'])
    queryset = models.ActionLog.objects.all().order_by('-timestamp')
    serializer_class = serializers.ActionLogSerializer
    permission_classes = [
        api_key_permissions.HasAPIKey
    ]


class MAVPView(generics.ListCreateAPIView):
    schema = AutoSchema(tags=['Administration'])
    queryset = models.MAVP.objects.all()
    serializer_class = serializers.MAVPSerializer
    permission_classes = [
        HasAPIKeyOrReadOnly
    ]


class MAVPDeleteView(generics.DestroyAPIView):
    schema = AutoSchema(tags=['Administration'])
    queryset = models.MAVP.objects.all()
    serializer_class = serializers.MAVPSerializer
    permission_classes = [
        api_key_permissions.HasAPIKey
    ]
