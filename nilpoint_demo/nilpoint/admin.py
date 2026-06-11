from django.contrib import admin

from .models import Player, PlayerCharacter


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    model = Player


@admin.register(PlayerCharacter)
class PlayerCharacterAdmin(admin.ModelAdmin):
    model = PlayerCharacter
