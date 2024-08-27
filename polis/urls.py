from django.urls import include, path
from polis import views


urlpatterns = [
    path(
        "c/<str:slug>",
        views.PolisConversationView.as_view(),
        name="conversation",
    ),
    path(
        "c/r/<str:slug>",
        views.PolisConversationReportView.as_view(),
        name="conversation_report",
    ),
    path(
        "p",
        views.ParticipantView.as_view(),
        name="participant_create",
    ),
    path(
        "p/update/<uuid:pk>",
        views.PerticipantUpdateView.as_view(),
        name="participant_update",
    ),
    path(
        "p/login",
        views.LoginView.as_view(),
        name="participant_login",
    ),
    path(
        "p/logout",
        views.LogoutView.as_view(),
        name="participant_logout",
    ),
    path("c", views.HomeView.as_view(), name="home"),
    path("__reload__/", include("django_browser_reload.urls")),
]
