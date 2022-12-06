from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Password


class DuserAdmin(UserAdmin):

    list_display = (
        "id",
        "username",
        "phone_number",
        "email",
        "first_name",
        "last_name",        
        "last_login",
        "update_count",
        "is_active",
        "is_staff",
        "is_trusted",
        "is_superuser"
    )

    list_display_links = ("id","username")
    search_fields = ("phone_number","email","username","email",)
    ordering = ("id",)

    list_filter = ("username","phone_number","last_login","update_count","is_active")

    list_editable = (
        "phone_number",        
        "email",
        "update_count",
        "is_active"
    )
    readonly_fields = ("password",)


admin.site.register(User, DuserAdmin)


class PasswordAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "password",
        "created_at",
        "updated_at"
    )

    list_display_links = ("id","username","created_at","updated_at")
    search_fields = ("username","email","created_at",)
    ordering = ("id",)

    list_filter = ("username","created_at")


    readonly_fields = ("password","username")


admin.site.register(Password, PasswordAdmin)
