from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        # Check if 'next' parameter exists in the request
        next_url = request.GET.get("next")
        if next_url:
            return next_url
        # Fallback to the default redirect URL
        return super().get_login_redirect_url(request)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        # Check if 'next' parameter exists in the request
        next_url = request.GET.get("next")
        if next_url:
            return next_url
        # Fallback to the default redirect URL
        return super().get_connect_redirect_url(request, socialaccount)
