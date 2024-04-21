from django.urls import path
from . import views

urlpatterns = [
    # Provide endpoint for searchin API
    path('search/', views.search_repositories, name='search_repositories'),
]
