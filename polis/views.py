import logging

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    FormView,
)

from .forms import ParticipantForm, ContactForm
from .models import Conversation, Participant
from allauth.socialaccount.adapter import get_adapter
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


class ParticipantMixin(object):
    participant = None
    authenticated_user = None

    def get_session_id(self, request):
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key

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
        session_id = self.get_session_id(request)
        self.authenticated_user = (
            request.user if request.user and request.user.is_authenticated else None
        )
        user_participant = self.get_from_user(self.authenticated_user)
        cookie_participant = self.get_from_cookies(request)

        if self.authenticated_user and user_participant and cookie_participant:
            logger.info(
                f"[Session: {session_id}] User is authenticated and has a participant_id cookie"
            )
            if user_participant != cookie_participant:
                logger.info(
                    f"[Session: {session_id}] User is authenticated and has a different participant_id cookie, merging participants"
                )
                # merge the two participants
                user_participant.merge(cookie_participant)
                cookie_participant.delete()

            self.participant = user_participant
        elif self.authenticated_user and cookie_participant:
            logger.info(
                f"[Session: {session_id}] User is authenticated and has a participant_id cookie"
            )
            # The participant started the conversation without being logged in and now logs in
            self.participant = cookie_participant
            self.participant.assign_user(self.authenticated_user)
        elif self.authenticated_user and user_participant:
            logger.info(
                f"[Session: {session_id}] User is authenticated and has a participant"
            )
            self.participant = user_participant
        elif cookie_participant:
            logger.info(
                f"[Session: {session_id}] User is not authenticated and has a participant_id cookie"
            )
            self.participant = cookie_participant

        if self.participant:
            logger.info(f"[Session: {session_id}] User {self.participant} wins")
            self.participant.refresh_xid_metadata()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participant"] = self.participant
        return context


class MainHomeView(ParticipantMixin, FormView):
    template_name = "main_home.html"
    form_class = ContactForm

    def get_conversaciones(self):
        queryset = Conversation.objects.filter(show_in_list=True)
        return queryset

    def get_success_url(self):
        return reverse("main_home") + "#contacto"

    def form_valid(self, form):
        name = form.cleaned_data.get("name")
        email = form.cleaned_data.get("email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        full_message = f"""
            Received message below from {name} {email}
            ________________________
            Asunto: {subject}

            {message}
            """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        # success message
        messages.success(self.request, _("Mensaje enviado correctamente"))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conversaciones"] = self.get_conversaciones()
        context["slider_conversaciones"] = len(context["conversaciones"]) > 1
        return context


class HomeView(ParticipantMixin, ListView):
    template_name = "pages/home.html"
    model = Conversation

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(show_in_list=True)
        return queryset

    def get(self, request, *args, **kwargs):
        self.init_participant(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slider_conversaciones"] = len(context["object_list"]) > 1
        return context


class ParticipantView(ParticipantMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "pages/participant_form.html"
    next = None

    def get_initial(self):
        initial = super().get_initial()
        if self.participant and self.participant.user:
            initial["name"] = self.participant.user.get_full_name()
            initial["email"] = self.participant.user.email
        return initial

    def get(self, request, *args, **kwargs):
        session_id = self.get_session_id(request)
        self.next = request.GET.get("next")
        logger.info(f"[Session: {session_id}] GET ParticipantView, next: {self.next}")
        self.init_participant(request)
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
        session_id = self.get_session_id(request)
        self.next = request.GET.get("next")
        logger.info(f"[Session: {session_id}] POST ParticipantView, next: {self.next}")
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        session_id = self.get_session_id(self.request)
        logger.info(
            f"[Session: {session_id}] POST ParticipantView form_invalid: {form.errors}"
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        session_id = self.get_session_id(self.request)
        self.participant = form.save()
        logger.info(
            f"[Session: {session_id}] POST ParticipantView created: {self.participant}, next: {self.next}"
        )
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
                logger.info(f"[Session: {session_id}] Provider: {provider}")
                redirect_url = provider.get_login_url(self.request, next=self.next)
                response = redirect(redirect_url)

        self.set_cookie(response)  # Set a cookie for one year
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ParticipantUpdateView(ParticipantMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "pages/participant_update_form.html"
    next = None

    def get(self, request, *args, **kwargs):
        self.init_participant(request)
        self.next = request.GET.get("next")
        if not self.participant or self.get_object() != self.participant:
            logger.info(
                f"[Session: {self.get_session_id(request)}] Participant not found or mismatch, redirecting to home"
            )
            if self.next:
                return redirect(self.next)
            else:
                return redirect("home")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("home")

    def post(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        session_id = self.get_session_id(self.request)
        form.save()
        self.get_object().refresh_xid_metadata()
        logger.info(f"[Session: {session_id}] Participant updated: {self.get_object()}")

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
                logger.info(f"[Session: {session_id}] Provider: {provider}")
                redirect_url = provider.get_login_url(self.request, next=self.next)
                response = redirect(redirect_url)

        self.set_cookie(response)  # Set a cookie for one year
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(TemplateView):
    template_name = "pages/login_form.html"

    def get_success_url(self):
        return reverse("polis::home")

    def post(self, request, *args, **kwargs):
        session_id = self.get_session_id(request)
        response = HttpResponseRedirect(self.get_success_url())
        response.set_cookie("participant_id", self.participant.id, max_age=31536000)
        logger.info(
            f"[Session: {session_id}] User logged in, participant_id set in cookie"
        )
        return response


class LogoutView(ParticipantMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        session_id = self.get_session_id(request)
        response = HttpResponseRedirect(reverse("home"))
        response.delete_cookie("participant_id")
        logout(request)
        logger.info(
            f"[Session: {session_id}] User logged out, participant_id cookie deleted"
        )
        return response


class PolisConversationView(ParticipantMixin, DetailView):
    template_name = "pages/conversation.html"
    model = Conversation
    participant = None

    def get(self, request, *args, **kwargs):
        session_id = self.get_session_id(request)
        self.init_participant(request)
        if not self.participant:
            # Add next parameter to redirect to the conversation after login
            response = redirect("participant_create")
            response["Location"] += f"?next={request.path}"
            logger.info(
                f"[Session: {session_id}] No participant found, redirecting to participant_create"
            )
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
