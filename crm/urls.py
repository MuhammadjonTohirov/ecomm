from django.urls import path, include
from rest_framework import routers

from crm.views import views, views_auth, login_view
from crm.views.dashboard_view import crm_dashboard, get_organizations, get_clients, get_employees, client_detail, employee_detail
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()

router.register('bank', viewset=views.BankViewSet)
router.register('organization', viewset=views.OrganizationViewSet)

urlpatterns = [
    # Dashboard UI routes
    path('dashboard/', crm_dashboard, name='crm_dashboard'),
    path('clients/<int:client_id>/', client_detail, name='client_detail'),
    path('employees/<int:employee_id>/', employee_detail, name='employee_detail'),
    
    # API routes for dashboard
    path('api/organizations/', get_organizations, name='get_organizations'),
    path('api/clients/', get_clients, name='get_clients'),
    path('api/employees/', get_employees, name='get_employees'),
]

urlpatterns += [
    path('init_defaults', views.init_default),
    path('register', views.register),
    path('api/', include(router.urls)),
    path('api/login/', login_view.login_view),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views_auth.new_token, name='token_refresh'),
    path('api/token/verify/', views_auth.verify_token, name='token_verify'),
    path('app/config', views.get_config),
    path('api/search_clients', views.search_clients),
]