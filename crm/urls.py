from django.urls import path, include
from rest_framework import routers

from crm.views import views, views_auth, login_view
from crm.views.dashboard_view import crm_dashboard, get_organizations, get_employees, employee_detail
from rest_framework_simplejwt import views as jwt_views
from crm.views.salary_attendance_views import (
    check_in,
    check_out,
    get_attendance_report,
    set_employee_salary,
    get_current_salary,
    calculate_salary_period
)

router = routers.DefaultRouter()

router.register('bank', viewset=views.BankViewSet)
router.register('organization', viewset=views.OrganizationViewSet)

urlpatterns = [
    # Dashboard UI routes
    path('dashboard/', crm_dashboard, name='crm_dashboard'),
    path('employees/<int:employee_id>/', employee_detail, name='employee_detail'),
    
    # API routes for dashboard
    path('api/organizations/', get_organizations, name='get_organizations'),
    path('api/employees/', get_employees, name='get_employees'),
    
    # Attendance endpoints
    path('api/attendance/check-in/', check_in, name='employee_check_in'),
    path('api/attendance/check-out/', check_out, name='employee_check_out'),
    path('api/attendance/report/', get_attendance_report, name='attendance_report'),
    
    # Salary endpoints
    path('api/salary/set/', set_employee_salary, name='set_employee_salary'),
    path('api/salary/current/', get_current_salary, name='get_current_salary'),
    path('api/salary/calculate/', calculate_salary_period, name='calculate_salary_period'),
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
    path('api/get_employees_by_organization/', views.get_employees_by_organization, name='get_employees_by_organization'),
]