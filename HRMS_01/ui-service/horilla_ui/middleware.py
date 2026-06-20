"""JWT session middleware - stores access token in session."""

from django.shortcuts import redirect


class JWTSessionMiddleware:
    """Redirect unauthenticated users to login.

    Exempt paths: login itself, static files, media files, and admin.
    """

    EXEMPT_PREFIXES = (
        "/login/",
        "/logout/",
        "/forgot-password/",
        "/reset-password/",
        "/signup/",
        "/static/",
        "/media/",
        "/admin/",
        "/favicon.ico",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self._is_exempt(request.path):
            if not request.session.get("access_token"):
                return redirect("login")
        return self.get_response(request)

    def _is_exempt(self, path: str) -> bool:
        return any(path.startswith(p) for p in self.EXEMPT_PREFIXES)
