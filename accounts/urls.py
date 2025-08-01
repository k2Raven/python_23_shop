from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, ProfileView, UserChangeView, UserPasswordChangeView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='registration'),
    path('<int:pk>/profile/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/profile/change/', UserChangeView.as_view(), name='change-profile'),
    path('<int:pk>/profile/change-password/', UserPasswordChangeView.as_view(), name='change-password'),

]
