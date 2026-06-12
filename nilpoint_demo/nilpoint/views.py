from django.views.generic import View
from django.shortcuts import redirect  # , render
from .models import Game
from django.http import HttpResponseNotFound, HttpResponse


class NilpointDebugView(View):
    """Debug view, can be used to drop in to places before the views
    are ready, ensuring everythng else is doing what is expected"""

    def get(self, request, *args, **kwargs):
        content = "Nilpoint Debug Page\n"
        content += "===================\n\n"
        content += f"{request.method} : {request.path}\n\n"
        content += "*args\n-----\n\n"
        for i in args:
            content += f"    {i}\n"
        content += "\n"
        content += "**kwargs\n--------\n\n"

        for k in kwargs:
            content += f"    {k} : {kwargs[k]}\n"
        content += "\n"
        content += f"GET: {request.GET}\n\n"
        content += f"POST: {request.POST}\n\n"
        content += f"COOKIES: {request.COOKIES}\n\n"
        content += f"USER: {request.user}\n\n"
        return HttpResponse(content, content_type="text/plain")


class NilpointRootView(View):
    def get(self, request, *args, **kwargs):
        return redirect("home")


class NilpointGameDispatchView(View):
    """Dispatch requests for Nilpointgames.

    Combining the nilpoint_slug (identifies a unique instance of a game) and
    the game object _game_type (identifies the game uniquely) gives us
    a way to generate unique URLs that can be served by the game apps.

    The games will be expected to use the namespace of their Game
    class, all lowercase.  For example MyFirstGame is 'myfirstgame'
    and if the instance has the nilpoint_slug 'hello-world' then this
    identifies the instace of MyFirstGame.  The urls will then be
    expected to have the namespace 'myfirstgame' with the keyword arg
    'nilpoint_slug' set to 'hello-world'. A game-level dispatcher should pick up the following url names:

     - dispatch (for example the name could be 'myfirstgame:dispatch'
       and the request will include the nilpoint_slug as a keyword
       argument. The URL might actually be
       'games/myfirstgame/hello-world/dispatch'.

    """

    def get(self, request, *args, **kwargs):

        slug = kwargs.get("nilpoint_slug")
        try:
            game = Game.objects.get(nilpoint_slug=slug)
            game = game.get_real_instance()
            namespace = game._game_type

            return redirect(f"{namespace}:dispatch", nilpoint_slug=game.nilpoint_slug)

        except Game.DoesNotExist:
            return HttpResponseNotFound(
                f"We don't seem to have a game usingthe slig '{slug}'!"
            )
        return redirect("home")
