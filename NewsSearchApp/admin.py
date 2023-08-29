from django.contrib import admin
from .models import UserSearch, SearchResult
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count



class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    actions = ['block_users', 'unblock_users']

    def block_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected users have been blocked.")

    def unblock_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected users have been unblocked.")

    block_users.short_description = "Block selected users"
    unblock_users.short_description = "Unblock selected users"


@admin.register(UserSearch)
class UserSearchAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'date_searched', 'user')
    list_filter = ('date_searched',)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request, extra_context=extra_context)

        # Get trending keywords
        trending_keywords = UserSearch.objects \
            .filter(date_searched__gte=(timezone.now() - timedelta(days=7))) \
            .values('keyword') \
            .annotate(search_count=Count('keyword')) \
            .order_by('-search_count')[:10]

        response.context_data['trending_keywords'] = trending_keywords

        return response
    

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# admin.site.register(UserSearch)
admin.site.register(SearchResult)
