from django.contrib import admin
from .models import User, Profile


class ProfileAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProfileAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['followers'].required = False
        return form


admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
