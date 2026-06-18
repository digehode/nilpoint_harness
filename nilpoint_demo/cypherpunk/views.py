from django.http import HttpResponse

from nilpoint.views import NilpointGameBasic


class CypherpunkGameView(NilpointGameBasic):
    handlers = {"test": "test_view"}
    # landing_partial = "cypherpunk/landing.jinja2#landing"

    def test_view(self, request, *args, **kwargs):
        return HttpResponse("This worked", content_type="text/plain")
