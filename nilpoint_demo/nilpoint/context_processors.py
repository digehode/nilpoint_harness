from .models import Game, Player


class NilpointContext:
    """A custom, non-ORM class built dynamically per-request."""

    def __init__(self, request):
        # if request.user.is_authenticated:
        #     # Example: fetching active tasks or items related to the user
        #     # (Using a hypothetical filter or method)
        #     self.active_items = ["Task 1", "Task 2", "Task 3"]
        #     self.user_role = "Admin" if request.user.is_staff else "Member"
        # else:
        #     self.active_items = []
        #     self.user_role = "Guest"

        self.games = [game.get_real_instance() for game in Game.objects.all()]
        self.player = Player.objects.get(user=request.user)


def nilpoint_context(request):
    return {"nilpoint": NilpointContext(request)}
