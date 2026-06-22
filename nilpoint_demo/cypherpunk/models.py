from django.db import models
from nilpoint.models import Game, PlayerCharacter


class CypherpunkGame(Game):
    name = "Cypherpunk: Crouching Cypher, Hidden Punk"
    description = "Cypherpunk is a game of encryption and decryption. Enter a world of stuff, where things happen and people do things."


class CypherpunkPC(PlayerCharacter):
    pass


class Deck(models.Model):
    """Represents the comms deck of a player character


    TODO: individual deck settings in here? Volume, for eg?
    """

    player_character = models.OneToOneField(
        CypherpunkPC, null=False, on_delete=models.CASCADE, related_name="deck"
    )


class Module(models.Model):
    """Superclass for specific modules"""

    background_image = "cypherpunk/modules/generic.png"

    # game = models.ForeignKey(
    #     Game, null=False, on_delete=models.CASCADE, related_name="locations"
    # )
