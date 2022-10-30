from django.contrib import admin
from authentications.models import Users
# Register your models here.

@admin.register(Users)
class Useradmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email_address")
    