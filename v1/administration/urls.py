from django.urls import include, path

from v1.administration import views


urlpatterns = [
    path('action-log/', include([
        path('new', views.new_action_log, name='action-log-new'),
        path('all', views.get_action_logs, name='action-log-all')
    ])),
    path('mavp/', include([
        path('all', views.get_mavp, name='mavp-all'),
        path('new', views.new_mavp, name='mavp-new'),
        path('delete', views.delete_mavp, name='mavp-delete')
    ]))
]
