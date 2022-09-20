"""mailing_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
#from rest_framework_swagger.views import get_swagger_view

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from mailing_app.views import ClientData, ClientDataDetail, MailingData, MailingDataDetail, MailingDataStats, MailingDataDetailStats


schema_view = get_schema_view(
    openapi.Info(
        title="Mailing service API",
        default_version='v1',
        description="Welcome to the mailing service API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),


    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    path('api/v1/clients', ClientData.as_view()),
    path('api/v1/clients/<int:pk>', ClientDataDetail.as_view()),
    path('api/v1/mailings', MailingData.as_view()),
    path('api/v1/mailings/stats', MailingDataStats.as_view()),
    path('api/v1/mailings/<int:pk>', MailingDataDetail.as_view()),
    path('api/v1/mailings/<int:pk>/stats', MailingDataDetailStats.as_view()),
    #path('api/v1/messages', MessageData.as_view()),
]
