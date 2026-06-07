# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import View


class BaseView(View):
    context = {}

    def _render(self, request):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        return self._render(request)


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
            print(form.cleaned_data)
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            print(f"Creating user with u/p: {username}/{password}")
            User = get_user_model()
            new_user = User.objects.create_user(username=username, password=password)
            new_user.save()
            return redirect("login")
        else:
            print("Invalid form")
        return self.get(request, *args, **kwargs)


class LoginView(BaseView):
    template_name = "login.jinja2"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        self.context["form"] = AuthenticationForm
        return self._render(request)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("User already auth'd")
            return redirect("home")
        form = AuthenticationForm(None, request.POST)
        print(request.POST)
        if form.is_valid():
            print("Valid form")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(f"Got u/p: {username}/{password}")

            user = authenticate(request=request, username=username, password=password)
            if not user:
                print("No user")
                return redirect("login")
            print("Authenticated?")
            login(request, user)
            return redirect("home")
        else:
            print("Invalid form")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(f"Got u/p: {username}/{password}")

            print(f"[{form.errors}]")
        return redirect("login")
