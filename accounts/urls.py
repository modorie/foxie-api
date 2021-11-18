from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.profile_detail_or_update),
    path('<str:username>/follow/', views.follow),
]
