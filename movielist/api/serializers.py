from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Movie, UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'userprofile']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['url', 'id', 'user', 'movielist']

class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ['url', 'id', 'title', 'rating', 'release_date', 'description', 'genres', 'playtime', 'imdb_url', 'jw_link']