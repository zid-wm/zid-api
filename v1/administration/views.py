from rest_framework import generics, permissions
from rest_framework.schemas.openapi import AutoSchema

from v1.administration import models, serializers


class ActionLogView(generics.ListCreateAPIView):
    schema = AutoSchema(tags=['Administration'])
    queryset = models.ActionLog.objects.all().order_by('-timestamp')
    serializer_class = serializers.ActionLogSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class MAVPView(generics.ListCreateAPIView):
    schema = AutoSchema(tags=['Administration'])
    queryset = models.MAVP.objects.all()
    serializer_class = serializers.MAVPSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class MAVPDeleteView(generics.DestroyAPIView):
    schema = AutoSchema(tags=['Administration'])
    queryset = models.MAVP.objects.all()
    serializer_class = serializers.MAVPSerializer
    permission_classes = [
        permissions.AllowAny
    ]
