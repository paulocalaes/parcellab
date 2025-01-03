"""project_parcellab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

schema_view = get_schema_view(
   openapi.Info(
      title="Parcellab API",
      default_version='v1',
      description="API Documentation",
      terms_of_service="https://www.parcellab.com/terms/",
      contact=openapi.Contact(email="contact@parcellab.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[TokenAuthentication]
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<str:version>/', include([
        path('shipments/', include('shipments.urls')),
        path('weather/', include('weather.urls')),
        path('articles/', include('articles.urls')),

        # path('auth/', include('djoser.urls')),  
        # path('auth/', include('djoser.urls.authtoken')),
    ])),  

    # Rotas do Swagger
    re_path(r'^swagger/v1(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), {'version': 'v1'}, name='schema-json-v1'),
    path('swagger/v1/', schema_view.with_ui('swagger', cache_timeout=0), {'version': 'v1'}, name='schema-swagger-ui-v1'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]