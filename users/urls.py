from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('login/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('register/',RegisterAPIView.as_view(),name='sign_up'),
    path('status/',UserIdentityAPIView.as_view(),name='user_status'),
    path('staff/',UserStaffListAPIView.as_view(),name='user_staff'),
    path('change_password/',ChangePasswordAPIView.as_view(),name='change_password'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]