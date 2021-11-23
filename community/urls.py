from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    # POST /articles/
    # GET /articles/
    path('community/', views.article_list),
    path('community/new/', views.article_create),
    # GET /articles/1/
    # PUT /articles/1/
    # DELETE /articles/1/
    path('community/<int:article_pk>/', views.article_detail),
    path('community/<int:article_pk>/edit/', views.article_update_or_delete),
    path('community/<int:article_pk>/likes/', views.article_likes),
    # POST /articles/1/comments/
    path('community/<int:article_pk>/comments/', views.comment_list),
    path('community/<int:article_pk>/comments/new/', views.comment_create),
    # PUT /articles/1/comments/1/
    # DELETE /articles/1/comments/1/
    path('community/<int:article_pk>/comments/<int:comment_pk>/', views.comment_update_or_delete),
    path('community/<int:article_pk>/comments/<int:comment_pk>/likes/', views.comment_likes),
]