
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("employees.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("helpdesk.urls")),
]
