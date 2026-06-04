"""Core models for nilpoint"""

from django.contrib.auth import get_user_model
from django.db import models


class Game(models.Model):
    """The top-level Game object, to which all other game items will refer."""

    name = models.CharField(max_length=100, null=False, blank=False)


class Player(models.Model):
    """Represents a player

    Refers to a user for uniquely identifying the person

    Contains all aspects that are not specific to a single game that
    are not part of the user model

    """

    user = models.ForeignKey(
        get_user_model(),
        null=False,
        on_delete=models.CASCADE,
    )

    handle = models.CharField(max_length=100, null=False, blank=False)
