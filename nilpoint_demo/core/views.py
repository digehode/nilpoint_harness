# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages
from nilpoint.models import Player, Game


class BaseView(View):
    context = {}

    def _render(self, request):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        return self._render(request)


class GameLaunchView(View):
    def get(self, request, *args, **kwargs):
        # TODO parameterise these and pass to nilpoint? A setting?
        # TODO: error handling.
        slug = kwargs["nilpoint_slug"]
        # TODO: 404 on no matching slug
        game = Game.objects.get(nilpoint_slug=slug)
        return render(request, "home.jinja2", {"launch_game": game})


class HomeView(BaseView):
    template_name = "home.jinja2"


class NewUserView(BaseView):
    template_name = "newuser.jinja2"

    def get(self, request, *args, **kwargs):
        self.context["form"] = UserCreationForm
        return self._render(request)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            User = get_user_model()
            new_user = User.objects.create_user(username=username, password=password)
            new_user.save()
            new_player = Player(user=new_user)
            new_player.save()
            messages.add_message(request, messages.SUCCESS, f"User {username} created.")
            return redirect("login")
        messages.add_message(request, messages.WARNING, "Unable to create user.")
        self.context["form"] = form
        return self._render(request)


class LoginView(BaseView):
    template_name = "login.jinja2"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        self.context["form"] = AuthenticationForm
        return self._render(request)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        form = AuthenticationForm(None, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request=request, username=username, password=password)
            if not user:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Couldn't log in with that username/password",
                )
                return redirect("login")

            messages.add_message(request, messages.SUCCESS, f"Logged in as {user}")
            login(request, user)
            return redirect("home")
        else:
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            messages.add_message(
                request, messages.WARNING, "Couldn't log in with that username/password"
            )

        return redirect("login")


class LogoutView(BaseView):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, "Logged Out")
        return redirect("home")
