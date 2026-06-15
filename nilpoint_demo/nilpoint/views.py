from django.views.generic import View
from django.shortcuts import redirect, render
from .models import Game, Player, PlayerCharacter
from django.http import HttpResponseNotFound, HttpResponse
from . import NilpointMissingSlugException
from .forms import NewPlayerCharacterForm


# TODO: deal with no game set, etc in dispatch function
# TODO: decorators for GET only, POST only or both?


class NilpointGameBasic(View):
    """Super class for game views."""

    _handlers = {
        "debug": "debug",
        "overview": "handle_overview",
        "new_player_character": "handle_new_player_character",
    }

    def __init__(self, *args, **kwargs):
        """Combine subclass handlers with the _handlers dict"""
        if hasattr(self, "handlers"):
            self._handlers.update(self.handlers)
        self.game = None
        self.player = None
        self.player_characters = []
        super().__init__(*args, **kwargs)

    def get_player_characters(self, request, *args, **kwargs):
        if self.game is not None and request.user and not request.user.is_anonymous:
            return self.game.get_player_characters(request.user, self.game)
        return None

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

    def get_context_data(self, request, *args, **kwargs):
        context = {}

        context["game"] = self.game
        context["player_characters"] = self.player_characters

        return context

    def nilpoint_render(self, request, template, context={}, *args, **kwargs):
        full_context = {}

        full_context.update(self.get_context_data(request, *args, **kwargs))
        full_context.update(context)

        return render(request, template, context=full_context)

    def _get_post_common(self, request, *args, **kwargs):
        """Do all of the things that need to be done regardless of method

        1. Set the self.game object.
        2. Set the self.player object, or None if it doesn't exist
        3. Set self.player_characters to a list of player characters for this user, for this game
        3. set self.action
        4. If an early response is required (errors, for eg), return it
        """

        # TODO: make a decorator for the GET and POST functions that
        # use this and deal with the result so it removes the
        # duplication in those funcitons

        if Player.objects.filter(user=request.user).exists():
            self.player = request.user.player
        else:
            self.player = None

        try:
            self.game = self.get_game_object(request, *args, **kwargs)
        except Game.DoesNotExist:
            self.game = None
        except NilpointMissingSlugException:
            self.game = None

        if self.player is not None and self.game is not None:
            self.player_characters = self.get_player_characters(
                request, *args, **kwargs
            )

        self.action = request.GET.get("action", None)
        if self.action is None:
            return HttpResponse("Action required", content_type="text/plain")
        if self.action not in self._handlers:
            return HttpResponse(
                f"Unknown action '{self.action}'", content_type="text/plain"
            )
        return None

    def get(self, request, *args, **kwargs):
        """GET dispatcher

        Uses the content of self.handlers to redirect requests to appropriate methods.
        """
        response = self._get_post_common(request, *args, **kwargs)
        if response:
            return response
        response = getattr(self, self._handlers[self.action])(request, *args, **kwargs)
        return response

    def post(self, request, *args, **kwargs):
        """GET dispatcher

        Uses the content of self.handlers to redirect requests to appropriate methods.
        """
        response = self._get_post_common(request, *args, **kwargs)
        if response:
            return response
        response = getattr(self, self._handlers[self.action])(request, *args, **kwargs)
        return response

    def _value_from_subclass_or_default(self, name, default):
        """Templates used in basic methods can be overridden by
        subclasses simply by adding class variables in the subclass.

        This method checks if 'name' exists and returns it if it does,
        else returns the default. It is used by the methods that check
        for overridden templates from subclasses.

        """

        if hasattr(self, name):
            return getattr(self, name)
        else:
            return default

    def handle_overview(self, request, *args, **kwargs):
        """Page overview

        Override the 'partial' used to render the content.
        """

        partial = self._value_from_subclass_or_default(
            "overview_partial", "nilpoint/game_overview.jinja2#game_overview"
        )

        return self.nilpoint_render(request, partial, context={}, *args, **kwargs)

    def handle_new_player_character(self, request, *args, **kwargs):
        """Handles new player character creation. By default, displays
        a form on a GET request and processes it on POST.

        Uses self.new_player_character_partial as a template if it
        exists, or the default Nilpoint template if not.

        Form submission is to the URL in
        self.new_player_character_submit or will use the default
        namespace rules if not.

        """

        partial = self._value_from_subclass_or_default(
            "new_player_character_partial",
            "nilpoint/new_player_character.jinja2#new_player_character",
        )
        message = None
        if self.player is None:
            message = "Your account is not a player account"
        if not self.game.allow_multiple_characters and len(self.player_characters) > 0:
            message = "You can't have more than one player character for this game"
        if message is not None:
            return self.nilpoint_render(
                request,
                partial,
                {"message": message},
                *args,
                **kwargs,
            )

        url = f"{self.game.get_url()}?action=new_player_character"
        url = self._value_from_subclass_or_default("new_player_character_submit", url)

        if request.method == "GET":
            form = NewPlayerCharacterForm()
            return self.nilpoint_render(
                request, partial, {"form": form, "submit_url": url}, *args, **kwargs
            )
        if request.method == "POST":
            form = NewPlayerCharacterForm(request.POST)

            # Add the game object to allow the form to do a narrower
            # check Without it, the form invalidates any duplicate
            # handle, regardless of which game it's used in
            form.game = self.game

            if form.is_valid():
                new_player_character = PlayerCharacter.objects.create(
                    player=self.player,
                    game=self.game,
                    handle=form.cleaned_data.get("handle"),
                )
                message = f"Your new player character '{new_player_character.handle}' has been created."
                return self.nilpoint_render(
                    request,
                    partial,
                    {"message": message},
                    *args,
                    **kwargs,
                )

                return HttpResponse("Valid", content_type="text/plain")
            else:
                return self.nilpoint_render(
                    request,
                    partial,
                    {"form": form, "submit_url": url},
                    *args,
                    **kwargs,
                )
        return HttpResponse("Method not implemented", content_type="text/plain")

    def debug(self, request, *args, **kwargs):
        """Debug view, can be used to drop in to places before the
        views are ready, ensuring everythng else is doing what is
        expected

        """
        return self.nilpoint_render(
            request,
            "nilpoint/debug.jinja2#debug",
            context={"request": request, "args": args, "kwargs": kwargs},
            *args,
            **kwargs,
        )


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
