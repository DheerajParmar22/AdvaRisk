from django.db import models
from django.contrib.auth.models import User

class UserSearch(models.Model):
    keyword = models.CharField(max_length=255)
    date_searched = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

class SearchResult(models.Model):
    user_search = models.ForeignKey(UserSearch, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    date_published = models.DateTimeField()
