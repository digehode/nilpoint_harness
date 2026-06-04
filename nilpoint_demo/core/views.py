from django.shortcuts import render
from django.views.generic import View


class BaseView(View):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class HomeView(BaseView):
    template_name = "home.jinja2"
