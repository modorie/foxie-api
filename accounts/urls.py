from django.urls import path
from . import views

from rest_framework_jwt.views import obtain_jwt_token

"""
FIX ME

- 'accounts/' URL 에 임시 연결
- API 주소로 변경 필요
"""

app_name = 'accounts'
urlpatterns = [
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('api-token-auth/', obtain_jwt_token),
    # path('delete/', views.delete, name='delete'),
    # path('update/', views.update, name='update'),
    # path('password/', views.change_password, name='change_password'),
    # path('<username>/', views.profile, name='profile'),
    # path('<int:user_pk>/follow/', views.follow, name='follow'),
]
