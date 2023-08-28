from django.contrib import admin

from .models import UserSearch, SearchResult

admin.site.register(UserSearch)
admin.site.register(SearchResult)