from django.shortcuts import redirect


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/admin/':
            return redirect("admin_dashboard")

        response = self.get_response(request)
        return response


__all__ = [
    "RedirectMiddleware"
]
