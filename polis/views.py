from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import ParticipantForm
from .models import Conversation, Participant


def home(request):
    return render(request, "pages/home.html", {})


def participant_view(request):
    # Check for a specific cookie to determine if the participant is returning
    participant = None
    if "participant_id" in request.COOKIES:
        participant_id = request.COOKIES["participant_id"]
        try:
            participant = Participant.objects.get(id=participant_id)
            # Load the participant data if found
            form = ParticipantForm(instance=participant)
        except Participant.DoesNotExist:
            form = ParticipantForm()
    else:
        form = ParticipantForm()

    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            response = redirect(
                "participant"
            )  # Redirect to a success page or another view
            response.set_cookie(
                "participant_id", participant.id, max_age=31536000
            )  # Set a cookie for one year
            return response

    conversation = None
    if participant:
        conversation = Conversation.objects.filter(
            instance=participant.instance
        ).first()
    context = {"form": form, "participant": participant, "conversation": conversation}

    return render(request, "pages/participant.html", context)


class HomeView(ListView):
    template_name = "pages/home.html"
    model = Conversation
    participant = None
    form = None

    def get(self, request, *args, **kwargs):
        if "participant_id" in request.COOKIES:
            participant_id = request.COOKIES["participant_id"]
            try:
                self.participant = Participant.objects.get(id=participant_id)
                self.form = ParticipantForm(instance=self.participant)
            except Participant.DoesNotExist:
                self.form = ParticipantForm()
        else:
            self.form = ParticipantForm()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["participant"] = self.participant
        return context


class ParticipantView(CreateView):
    model = Participant
    form_class = ParticipantForm

    def form_valid(self, form):
        participant = form.save()
        response = HttpResponseRedirect(reverse("home"))  # Change to your success URL
        response.set_cookie(
            "participant_id", participant.id, max_age=31536000
        )  # Set a cookie for one year
        return response


class PolisConversationView(DetailView):
    template_name = "pages/conversation.html"
    model = Conversation
    participant = None

    def get(self, request, *args, **kwargs):
        if "participant_id" in request.COOKIES:
            participant_id = request.COOKIES["participant_id"]
            try:
                self.participant = Participant.objects.get(id=participant_id)
            except Participant.DoesNotExist:
                return redirect("home")
        else:
            return redirect("home")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participant"] = self.participant
        return context
