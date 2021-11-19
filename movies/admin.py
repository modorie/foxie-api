from django.contrib import admin
from .models import Actor, Director, Genre, Movie, Casting, Review, Comment


admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Casting)
admin.site.register(Review)
admin.site.register(Comment)
