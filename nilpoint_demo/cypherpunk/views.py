from django.http import HttpResponse

from nilpoint.views import NilpointGameBasic


class CypherpunkGameView(NilpointGameBasic):
    handlers = {"test": "test_view"}
    # landing_partial = "cypherpunk/landing.jinja2#landing"
    # TODO: Move this to a game config or a field of the game model?
    default_location_graphic = "cypherpunk/locations/00_none/simple.png"

    def test_view(self, request, *args, **kwargs):
        return HttpResponse("This worked", content_type="text/plain")
