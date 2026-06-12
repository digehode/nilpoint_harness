"""Core models for nilpoint"""

from django.contrib.auth import get_user_model
from django.db import models


class Game(models.Model):
    """The top-level Game object, to which all other game items will refer.

    Subclass to create new games. Override the 'get_name' function to
    identify the game. 'instance_name' is used to distinguish between
    multiple instances of the same game on a given server.

    """

    name = "Generic Game"
    description = "This is a generic game. You should be subclassing "
    "this to create actual games. Or, if you have and you're still seing "
    "this, make use of the 'get_real_instance' method to get the downcast "
    "version of this object."

    instance_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text="The name of this game instance",
    )

    instance_description = models.TextField(
        null=False,
        blank=True,
        help_text="Description of the game instance",
    )

    nilpoint_slug = models.SlugField(
        help_text="A unique string that identifies this game in URLs",
        null=False,
        unique=True,
    )

    # Game type holds the subclass to which this can be downcast
    _game_type = models.CharField(max_length=50, editable=False)

    def save(self, *args, **kwargs):
        """Checks and automatically sets, if necessary, the _game_type"""
        if not self._game_type:
            # Automatically set the type based on the class name
            self._game_type = self.__class__.__name__.lower()
        super().save(*args, **kwargs)

    def get_real_instance(self):
        """Dynamically fetch the game subclass instance of the Game object"""
        if hasattr(self, self._game_type):
            return getattr(self, self._game_type)
        return self

    def __str__(self):
        return f"{self.get_real_instance().name} - {self.instance_name}"


class Player(models.Model):
    """Represents a player

    Refers to a user for uniquely identifying the person

    Contains all aspects that are not specific to a single game that
    are not part of the user model.

    This should be subclassed to include any instance specific things.

    """

    user = models.OneToOneField(
        get_user_model(), null=False, on_delete=models.CASCADE, related_name="player"
    )

    def __str__(self):
        return self.user.username


class PlayerCharacter(models.Model):
    """Represents a player for a given game

    Refers to the generic Player and through that to a user.

    Links game-specific data such as preferences, progress, etc.

    Can be sub-classed for specific instances, but the goal is to keep
    this fairly generic and use foreign-keys in game-specific
    models/views/etc. to refer to the character.

    """

    handle = models.CharField(max_length=100, null=False, blank=False)
    player = models.ForeignKey(
        Player, null=False, on_delete=models.CASCADE, related_name="characters"
    )
    game = models.ForeignKey(
        Game, null=False, on_delete=models.CASCADE, related_name="player_characters"
    )
