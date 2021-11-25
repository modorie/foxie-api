from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    path('community/', views.article_list_or_create),
    path('community/popular/', views.article_popular),
    path('community/<int:article_pk>/', views.article_detail_update_or_delete),
    path('community/<int:article_pk>/likes/', views.article_likes),
    path('community/<int:article_pk>/comments/', views.comment_list_or_create),
    path('community/<int:article_pk>/comments/<int:comment_pk>/', views.comment_detail_update_or_delete),
    path('community/<int:article_pk>/comments/<int:comment_pk>/likes/', views.comment_likes),
]