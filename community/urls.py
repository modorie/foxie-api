from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    # POST /articles/
    # GET /articles/
    path('community/', views.article_list),
    path('community/', views.article_create),
    # GET /articles/1/
    # PUT /articles/1/
    # DELETE /articles/1/
    path('community/<int:article_pk>/', views.article_detail),
    path('community/<int:article_pk>/', views.article_update_or_delete),
    # POST /articles/1/comments/
    path('community/<int:article_pk>/comments/', views.comment_create_or_list),
    # PUT /articles/1/comments/1/
    # DELETE /articles/1/comments/1/
    path('community/<int:article_pk>/comments/<int:comment_pk>/', views.comment_update_or_delete),
]