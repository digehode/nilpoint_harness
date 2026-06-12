from django.http import HttpResponse

from nilpoint.views import NilpointGameBasic


class DebugView(NilpointGameBasic):
    handlers = {"test": "test_view"}

    def test_view(self, request, *args, **kwargs):
        return HttpResponse("This worked", content_type="text/plain")
