from django.urls import path,include
from user import views
from .views import *

app_name = 'user'

urlpatterns = [
    path('healthcheck/', views.HealthCheckAPI.as_view(), name='healthcheck'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('rolecreation/',RoleCreationAPIView.as_view(), name='rolecreation'),
    path('approveuser/', UserApprovalAPIView.as_view(), name='approve_user'),

]