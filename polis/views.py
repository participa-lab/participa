import logging

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)


from .forms import ParticipantForm, ParticipantUpdateForm
from .models import Conversation, Participant, Affinity, Territory
from allauth.socialaccount.adapter import get_adapter

logger = logging.getLogger(__name__)


class ParticipantMixin(object):
    participant = None
    authenticated_user = None

    def get_from_cookies(self, request):
        if "participant_id" in request.COOKIES:
            participant_id = request.COOKIES["participant_id"]
            try:
                return Participant.objects.get(id=participant_id)
            except Participant.DoesNotExist:
                return None
        return None

    def set_cookie(self, response):
        response.set_cookie(
            "participant_id", self.participant.id, max_age=31536000
        )  # Set a cookie for one year
        return response

    def get_from_user(self, user):
        if user and user.is_authenticated:
            try:
                return Participant.objects.get(user=user)
            except Participant.DoesNotExist:
                return None
        return None

    def init_participant(self, request):
        self.authenticated_user = (
            request.user if request.user and request.user.is_authenticated else None
        )
        user_participant = self.get_from_user(self.authenticated_user)
        cookie_participant = self.get_from_cookies(request)
        logger.info(
            f"authenticated_user: {self.authenticated_user}, user_participant: {user_participant}, cookie_participant: {cookie_participant}"
        )

        if self.authenticated_user and user_participant and cookie_participant:
            logger.info("User is authenticated and has a participant_id cookie")
            if user_participant != cookie_participant:
                logger.info(
                    "User is authenticated and has a different participant_id cookie"
                )
                # If the user is logged in and has a different participant_id cookie, we delete the cookie
                # response = HttpResponseRedirect(reverse("home"))
                # response.delete_cookie("participant_id")
                # return response
            # else:
            self.participant = user_participant
        elif self.authenticated_user and cookie_participant:
            logger.info("User is authenticated and has a participant_id cookie")
            # The participant started the conversation without being logged in and now logs in
            self.participant = cookie_participant
            self.participant.assign_user(self.authenticated_user)
        elif self.authenticated_user and user_participant:
            logger.info("User is authenticated and has a participant")
            self.participant = user_participant
        elif self.authenticated_user and not user_participant:
            logger.info("User is authenticated and has no participant")
            participant_data = request.session.get("participant_form_data")
            if participant_data:
                affinity_name = participant_data.pop("affinity")
                affinity = (
                    Affinity.objects.filter(name=affinity_name).first()
                    if affinity_name
                    else None
                )
                territory_name = participant_data.pop("territory")
                territory = (
                    Territory.objects.filter(name=territory_name).first()
                    if territory_name
                    else None
                )
                participant_data.update({"affinity": affinity, "territory": territory})
                del participant_data["login"]
                self.participant = Participant.objects.create(**participant_data)
                self.participant.assign_user(self.authenticated_user)
        elif cookie_participant:
            logger.info("User is not authenticated and has a participant_id cookie")
            self.participant = cookie_participant

        if self.participant:
            logger.info(f"User {self.participant} wins")
            self.participant.refresh_xid_metadata()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participant"] = self.participant
        return context


class HomeView(ParticipantMixin, ListView):
    template_name = "pages/home.html"
    model = Conversation

    def get(self, request, *args, **kwargs):
        self.init_participant(request)
        return super().get(request, *args, **kwargs)


class ParticipantView(ParticipantMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "pages/participant_form.html"
    participant_data = {}
    next = None

    def get_initial(self):
        initial = super().get_initial()
        if self.participant and self.participant.user:
            initial["name"] = self.participant.user.get_full_name()
            initial["email"] = self.participant.user.email
        else:
            if self.participant_data:
                initial = self.participant_data
            initial["login"] = "1"
        return initial

    def get(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        logger.info(f"GET ParticipantView, next: {self.next}")
        self.init_participant(request)
        self.participant_data = request.session.get("participant_form_data")
        if self.participant:
            # Consolidated participant, saving into cookies
            if self.next:
                response = redirect(self.next)
            else:
                response = redirect("home")
            return self.set_cookie(response)
        # else create a new one
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        logger.info(f"POST ParticipantView, next: {self.next}")
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        logger.info(f"ParticipantView form_invalid: {form.errors}")
        return super().form_invalid(form)

    def form_valid(self, form):
        logger.info(f"ParticipantView form_valid: {form.data}")
        self.participant = form.save()
        logger.info(f"ParticipantView created: {self.participant}, next: {self.next}")
        response = HttpResponseRedirect(reverse("home"))  # Change to your success URL
        if self.next:
            response = redirect(self.next)

        # get name login
        name_login = form.data.get("login")
        # name_login has the name of the provider
        # find the provider in the registry
        adapter = get_adapter()
        providers = adapter.list_providers(self.request)

        for provider in providers:
            if provider.name == name_login:
                logger.info(f"Provider: {provider}")
                redirect_url = reverse("socialaccount_login", args=[provider.id])
                # add next parameter
                redirect_url += f"?next={self.next}"
                response = redirect(redirect_url)

        self.set_cookie(response)  # Set a cookie for one year
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PerticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantUpdateForm
    template_name = "pages/participant_update_form.html"

    def get_success_url(self):
        return reverse("home")

    def form_valid(self, form):
        form.save()
        self.get_object().refresh_xid_metadata()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(TemplateView):
    template_name = "pages/login_form.html"

    def get_success_url(self):
        return reverse("polis::home")

    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect(self.get_success_url())
        response.set_cookie("participant_id", self.participant.id, max_age=31536000)


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        response = HttpResponseRedirect(reverse("home"))
        response.delete_cookie("participant_id")
        logout(request)
        return response


class PolisConversationView(ParticipantMixin, DetailView):
    template_name = "pages/conversation.html"
    model = Conversation
    participant = None

    def get(self, request, *args, **kwargs):
        self.init_participant(request)
        if not self.participant:
            # Add next parameter to redirect to the conversation after login
            response = redirect("participant_create")
            response["Location"] += f"?next={request.path}"
            return response

        response = super().get(request, *args, **kwargs)
        return self.set_cookie(response)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_report"] = True if self.get_object().get_report_url() else False
        return context


class PolisConversationHomeView(ParticipantMixin, DetailView):
    template_name = "pages/conversation_home.html"
    model = Conversation


class PolisConversationReportView(DetailView):
    template_name = "pages/report.html"
    model = Conversation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_url"] = self.get_object().get_report_url()
        return context
