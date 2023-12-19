from django.db import models
from polis import choices
import uuid
from django.utils.translation import gettext_lazy as _


class Instance(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __meta__(self):
        verbose_name = _("Instance")
        verbose_name_plural = _("Instances")


class Conversation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    polis_id = models.CharField(max_length=200)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def __meta__(self):
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")


class Territory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __meta__(self):
        verbose_name = _("Territory")
        verbose_name_plural = _("Territories")


class Affinity(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __meta__(self):
        verbose_name = _("Affinity")
        verbose_name_plural = _("Affinities")


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=choices.GENDER_CHOICES)
    year_of_birth = models.IntegerField()
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    affinity = models.ForeignKey(Affinity, on_delete=models.CASCADE)

    def __str__(self):
        return self.instance.name + " - " + self.affinity.name

    def __meta__(self):
        ordering = ["instance", "affinity"]
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
