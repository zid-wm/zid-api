"""
URL configuration for zid_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin', admin.site.urls),
    path('v1/', include([
        path('admin/', include('v1.administration.urls')),
        # path('event/', include('v1.event.urls')),
        # path('feedback/', include('v1.feedback.urls')),
        # path('news/', include('v1.news.urls')),
        # path('user/', include('v1.user.urls'))
    ]))
]
