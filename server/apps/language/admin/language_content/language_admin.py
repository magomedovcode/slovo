from django.contrib import admin
from apps.language.models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'code'
    )
    search_fields = (
        'name',
        'code'
    )
