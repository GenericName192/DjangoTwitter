from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meeps
# Register your models here.


admin.site.unregister(Group)

# Mixing Profile and User
class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name"] # The list of fields to display.
    inlines = [ProfileInline]

# Remove and readd Users to change them to having the list above. 
admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(Meeps)

