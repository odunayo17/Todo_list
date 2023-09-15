from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("todo_list.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]
