from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "role",
        "student_id",
        "phone",
        "is_verified",
        "is_staff",
        "is_active",
        "is_superuser",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "role",
        "is_verified",
        "is_staff",
        "is_superuser",
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "student_id",
        "phone",
    )

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        
        ("Personal Info", {
            "fields": (
                "first_name",
                "last_name",
                "phone",
                "profile_picture",
                "role",
                "student_id",
            )
        }),

        ("Face Recognition", {
            "fields": (
                "face_encoding",
                "face_encoding_version",
                "last_face_update",
            ),
            "classes": ("collapse",),
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "is_verified",
                "groups",
                "user_permissions",
            ),
        }),

        ("Timestamps", {
            "fields": (
                "last_login",
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "phone",
                "role",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")
