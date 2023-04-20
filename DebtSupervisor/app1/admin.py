from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from app1.models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    name = 'Profile'
    #ForeignKey name
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
