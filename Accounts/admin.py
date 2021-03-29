from django.contrib import admin
from Accounts.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display=['user', 'address', 'country']
	list_filter=['user',]

admin.site.register(UserProfile, UserProfileAdmin)
