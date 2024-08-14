"""participa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("consensos/", include("polis.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("allauth.urls")),
    path("", TemplateView.as_view(template_name="main_home.html"), name="main_home"),
    path(
        "about", TemplateView.as_view(template_name="main_quienes.html"), name="about"
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
