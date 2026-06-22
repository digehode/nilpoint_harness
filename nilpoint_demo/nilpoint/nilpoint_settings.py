from django.conf import settings


DEFAULTS = {
    "PlayerCharacter": "nilpoint.PlayerCharacter",
}


class AppSettings:
    def __init__(self):
        # Get user's overrides from the global settings.py
        self.user_settings = getattr(settings, "NILPOINT_SETTINGS", {})

    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError(f"Invalid setting: '{attr}'")

        try:
            return self.user_settings[attr]
        except KeyError:
            return DEFAULTS[attr]

    def get(self, setting):
        """Uses getattr but with a nicer name"""
        return self.__getattr__(setting)


# Instantiate so it can be imported elsewhere
nilpoint_settings = AppSettings()
