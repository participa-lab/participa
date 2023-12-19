from django.shortcuts import render, redirect
from .forms import ParticipantForm
from django.http import HttpResponseRedirect
from .models import Participant, Conversation
from django.urls import reverse
from django.views import View



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


class ParticipantView(View):
    template_name = "pages/participant.html"

    def get(self, request, *args, **kwargs):
        participant = None
        if "participant_id" in request.COOKIES:
            participant_id = request.COOKIES["participant_id"]
            try:
                participant = Participant.objects.get(id=participant_id)
                form = ParticipantForm(instance=participant)
            except Participant.DoesNotExist:
                form = ParticipantForm()
        else:
            form = ParticipantForm()

        conversation = None
        if participant:
            conversation = Conversation.objects.filter(
                instance=participant.instance
            ).first()

        context = {
            "form": form,
            "participant": participant,
            "conversation": conversation,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            response = HttpResponseRedirect(
                reverse("participant")
            )  # Change to your success URL
            response.set_cookie(
                "participant_id", participant.id, max_age=31536000
            )  # Set a cookie for one year
            return response

        # If the form is not valid, re-render the page with the form errors
        return render(request, self.template_name, {"form": form})
