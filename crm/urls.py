from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as rest_views
from rest_framework.routers import DefaultRouter

from crm import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()

router.register('profile', viewset=views.ProfileViewSet)
router.register('bank', viewset=views.BankViewSet)
router.register('organization', viewset=views.OrganizationViewSet)

urlpatterns = []

urlpatterns += [
    path('init_defaults', views.init_default),
    path('register', views.register),
    path('api/', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
