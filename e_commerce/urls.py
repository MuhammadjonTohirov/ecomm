"""e_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from e_commerce import settings
from e_commerce import views as ecommerce_views
from helpers.defaults import Defaults
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

admin.autodiscover()
admin.site.enable_nav_sidebar = True

schema_view = get_schema_view(
    openapi.Info(
        title="API documentation",
        default_version='v1',
        description="Documentation for my API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', ecommerce_views.login, name='login'),
    path('initializer/', ecommerce_views.initializer, name='initializer'),
    path('logout/', ecommerce_views.logout, name='logout'),
    path('', ecommerce_views.home, name='home'),
    path('register/', ecommerce_views.register, name='register'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('sales/', include('sales.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('crm/', include('crm.urls')),
    path('wms/', include('wms.urls')),
    path('sales/', include('sales.urls'))
]

Defaults.deploy()
