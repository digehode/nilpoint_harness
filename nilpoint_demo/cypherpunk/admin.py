from django.contrib import admin

from .models import CypherpunkGame


@admin.register(CypherpunkGame)
class CypherpunkGameAdmin(admin.ModelAdmin):
    model = CypherpunkGame
    prepopulated_fields = {"nilpoint_slug": ("instance_name",)}
