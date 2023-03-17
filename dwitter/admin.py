from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Dweet

admin.site.unregister(User) #this removes the Group model form default django admin interface

#Next, you’ll change the fields sdisplayed in the admin section of Django’s built-in User model. To do this, you need to first unregister it since the model comes registered by default. Then, you can re-register the default User model to limit which fields the Django admin should display.

class ProfileInLine(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username",]
    inlines = [ProfileInLine,]

admin.site.register(User, UserAdmin)
admin.site.register(Dweet)
admin.site.unregister(Group)