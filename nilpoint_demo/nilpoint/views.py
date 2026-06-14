from django.views.generic import View
from django.shortcuts import redirect, render
from .models import Game
from django.http import HttpResponseNotFound, HttpResponse
from . import NilpointMissingSlugException


class NilpointGameBasic(View):
    """Super class for game views."""

    _handlers = {"debug": "debug", "overview": "handle_overview"}

    def __init__(self, *args, **kwargs):
        """Combine subclass handlers with the _handlers dict"""
        if hasattr(self, "handlers"):
            self._handlers.update(self.handlers)
        super().__init__(*args, **kwargs)

    def get_game_object(self, request, *args, **kwargs):
        """Return the generic game object associated with this request.

        By default, it looks for the nilpoint_slug in the request path.

        Games/platforms that don't use this system will need to
        provide a different implementation of this method in their
        views.

        Will allow the Game.DoesNotExist exception to bubble up and
        should be caught from wherever this is called.

        Raises nilpoint.MissingSlugException if the slug doesn't identify a game instance

        """
        if "nilpoint_slug" in kwargs:
            return Game.objects.get(nilpoint_slug=kwargs["nilpoint_slug"])
        else:
            raise NilpointMissingSlugException("No nilpoint_slug was given in kwargs")

    def get(self, request, *args, **kwargs):
        """GET dispatcher

        Uses the content of self.handlers to redirect requests to appropriate methods.

        Ensures the self.game object is set to the downcast game in question"""

        # Retrieve the generic game object
        try:
            self.game = self.get_game_object(request, *args, **kwargs)
        except Game.DoesNotExist:
            return HttpResponseNotFound(
                f"We don't seem to have a game usingthe slig '{kwargs['nilpoint_slug']}'!"
            )
        except NilpointMissingSlugException:
            return HttpResponseNotFound("No nilpoint slug provided!")
        action = request.GET.get("action", None)
        if action is None or action not in self._handlers:
            return HttpResponse("Action required", content_type="text/plain")

        return getattr(self, self._handlers[action])(request, args, kwargs)

    def handle_overview(self, request, *args, **kwargs):
        """Page overview

        Override the 'partial' used to render the content.
        """
        if hasattr(self, "overview_partial"):
            partial = self.overview_partial
        else:
            partial = "nilpoint/game_overview.jinja2#game_overview"
        return render(request, partial, context={"game": self.game.get_real_instance()})

    def debug(self, request, *args, **kwargs):
        """Debug view, can be used to drop in to places before the
        views are ready, ensuring everythng else is doing what is
        expected

        """

        content = "Nilpoint Debug Page\n"
        content += "===================\n\n"
        content += f"Working on game: {self.game}\n\n"
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

        except Game.DoesNotExist:
            return HttpResponseNotFound(
                f"We don't seem to have a game usingthe slig '{slug}'!"
            )
        redir = redirect(game.get_url())
        return redir
