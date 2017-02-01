from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=155, unique=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Quote(models.Model):
    text = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name = "user_added")

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name = "user_favorites")
    quote = models.ForeignKey(Quote, related_name = "favorite_quote")
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('user', 'quote',)
