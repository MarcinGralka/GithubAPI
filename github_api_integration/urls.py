from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include urls from github_api app
    path('github/', include('github_api.urls')),
]

