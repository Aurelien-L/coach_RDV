from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_user, name='login'),     # URL vers la page de login
    path('logout/', views.logout_user, name='logout'),      # URL de logout
    path('register/', views.register_user, name='register'),      # URL vers la page d'inscription
    path('dashboard/', views.dashboard, name='dashboard')       # URL vers le dashboard (s'adapte selon coach / client)
]
