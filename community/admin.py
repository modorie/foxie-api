from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['like_users'].required = False
        return form


class CommentAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super(CommentAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['like_users'].required = False
        return form


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
