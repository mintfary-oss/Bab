from django.contrib import admin

from .models import AdminActionLog, Report, SiteSettings


@admin.register(Report)
class RA(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ["pk", "reporter", "target_type", "reason", "status", "created_at"]
    list_filter = ["status", "reason"]


@admin.register(AdminActionLog)
class ALA(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ["admin_user", "action_type", "created_at"]


@admin.register(SiteSettings)
class SSA(admin.ModelAdmin):  # type: ignore[type-arg]
    fieldsets = (
        ("Основные", {"fields": ("site_name", "site_description", "logo")}),
        (
            "Цвета",
            {"fields": ("primary_color", "secondary_color", "accent_color", "background_color")},
        ),
        ("Контент", {"fields": ("footer_text", "announcement", "maintenance_mode")}),
        ("Соцсети", {"fields": ("social_vk", "social_telegram")}),
        ("SEO", {"fields": ("meta_keywords", "meta_description")}),
        ("Модерация", {"fields": ("max_posts_per_day", "auto_moderate_new_users", "banned_words")}),
    )

    def has_add_permission(self, r):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, r, obj=None):
        return False
