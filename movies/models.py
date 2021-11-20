from django.db import models
from django.conf import settings

from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField


class Actor(models.Model):  # cast
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    profile_path = models.TextField(null=True)
    also_known_as = ArrayField(
        models.CharField(max_length=30),
    )

    def __str__(self):
        return f'{self.id}: {self.name}'


class Director(models.Model):  # crew
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    profile_path = models.TextField(null=True)
    also_known_as = ArrayField(
        models.CharField(max_length=30),
    )

    def __str__(self):
        return f'{self.id}: {self.name}'


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    adult = models.BooleanField()
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField(null=True)
    original_language = models.CharField(max_length=20)
    original_title = models.CharField(max_length=200)

    genre_ids = models.ManyToManyField(
        Genre,
        related_name='movies',
    )
    actors = models.ManyToManyField(
        Actor,
        related_name='movies',
    )
    directors = models.ManyToManyField(
        Director,
        related_name='movies',
    )

    backdrop_path = models.TextField(null=True)
    poster_path = models.TextField(null=True)
    video = models.BooleanField(default=False)
    videos = JSONField(blank=True)
    recommendations = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return f'{self.id}: {self.title}'


class Casting(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor_id = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='castings')
    credit_id = models.CharField(primary_key=True, max_length=30)
    character = models.TextField(null=True)

    def __str__(self):
        return f'{self.movie_id.title} : {self.actor_id.name} ({self.character} 역)'


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    rank = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s_likes',
        blank=True
    )

    def __str__(self):
        return f'{self.pk}: {self.title}'


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s'
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s_likes',
        blank=True
    )

    def __str__(self):
        return f'{self.pk} {self.content}'
