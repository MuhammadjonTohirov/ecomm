from django.urls import path, include
from rest_framework import routers

from crm.views import views, views_auth, login_view
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()

router.register('bank', viewset=views.BankViewSet)
router.register('organization', viewset=views.OrganizationViewSet)

urlpatterns = []

urlpatterns += [
    path('init_defaults', views.init_default),
    path('register', views.register),
    path('api/', include(router.urls)),
    path('api/login/', login_view.login_view),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views_auth.new_token, name='token_refresh'),
    path('api/token/verify/', views_auth.verify_token, name='token_verify'),
    path('app/config', views.get_config),
]
