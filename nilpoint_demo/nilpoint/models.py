"""Core models for nilpoint"""

from django.db import models


class Game(models.Model):
    """The top-level Game object, to which all other game items will refer."""

    name = models.CharField("Name", max_length=100, null=False, blank=False)


class Player(models.Model):
    """Represents a player character"""

    pass
