# urls.py
from django.urls import path, include, re_path
from .views import BusinesscategoryAPIView, ChangePasswordView, DeleteAccount, EmailOTPAuthentication,  Logout, RegisterView, LoginView, TokenRefreshView, TokenVerifyView, UserBusinessAPIView, UserProfileView

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(),
         name='token_obtain_pair'),
    path('user_profile/', UserProfileView.as_view()),
    path('logout/', Logout.as_view()),
    path('changepassword/', ChangePasswordView.as_view()),
    path('delete_user/', DeleteAccount.as_view()),
    re_path(r'^social/', include('drf_social_oauth2.urls', namespace='social')),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password_reset/', include('django_rest_passwordreset.urls')),
    path('email/verify/', EmailOTPAuthentication.as_view(), name='email_verify'),
    path('user-business/', UserBusinessAPIView.as_view(), name='email_verify'),
    path('business-category/', BusinesscategoryAPIView.as_view(), name='email_verify'),
]
