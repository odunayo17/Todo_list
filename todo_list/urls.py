from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("edit/<str:pk>/", views.update, name="update"),
    path("delete/<str:pk>/", views.delete, name="delete"),
    path("delete-account/", views.delete_account, name="delete_acc"),
]
