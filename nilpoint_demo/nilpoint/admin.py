from django.contrib import admin

from .models import Player, PlayerCharacter, Game


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    model = Player


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = [
        "instance_name",
        "_game_type",
        "instance_description",
        "nilpoint_slug",
        "get_url",
        "allow_multiple_characters",
    ]


@admin.register(PlayerCharacter)
class PlayerCharacterAdmin(admin.ModelAdmin):
    model = PlayerCharacter
    list_display = ["handle", "player", "game"]
