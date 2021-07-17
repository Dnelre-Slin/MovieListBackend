from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Movie(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    rating = models.FloatField()
    release_date = models.DateField()
    description = models.CharField(max_length=1000, blank=True, default='')
    genres = models.CharField(max_length=300, blank=True, default='')
    playtime = models.DurationField()
    imdb_url = models.URLField(blank=True)
    jw_link = models.URLField(blank=True)

    def set_genres(self, x):
        self.genres = ",".join(x)
    def get_genres(self, x):
        return x.split(",")

    class Meta:
        ordering = ['title']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movielist = models.ManyToManyField(
        Movie,
        verbose_name=_('movies'),
        blank=True,
        help_text=_('The movies belonging to this movielist.'),
        related_name="profile",
        related_query_name="profile",
    )