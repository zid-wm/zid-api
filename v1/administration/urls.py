from django.urls import path

from v1.administration import views


urlpatterns = [
    path('action-log', views.ActionLogView.as_view(), name='action-log'),
    path('mavp', views.MAVPView.as_view(), name='mavp'),
    path('mavp/<str:pk>', views.MAVPDeleteView.as_view(), name='mavp-delete')
]
