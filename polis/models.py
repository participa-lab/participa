import datetime
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from polis import choices


class MillisField(models.BigIntegerField):
    def to_python(self, value):
        if value is None:
            return value
        return datetime.datetime.fromtimestamp(value / 1000.0)

    def get_prep_value(self, value):
        if value is None or isinstance(value, int):
            return value
        return int(value.timestamp() * 1000)


class Instance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    site_id = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id} {self.name}"

    class Meta:
        verbose_name = _("Instance")
        verbose_name_plural = _("Instances")


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=200)
    slug = models.SlugField(default="", null=False)
    description = models.TextField()

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)

    border = models.CharField(max_length=200, blank=True, null=True)
    border_radius = models.CharField(max_length=200, blank=True, null=True)
    padding = models.CharField(max_length=200, blank=True, null=True)
    height = models.CharField(max_length=200, blank=True, null=True)
    ui_language = models.CharField(max_length=200, blank=True, null=True)
    dwok = models.CharField(max_length=200, blank=True, null=True)

    show_visualization = models.BooleanField(default=True)
    show_share = models.BooleanField(default=True)
    bg_white = models.BooleanField(default=False)

    auth_needed_to_vote = models.BooleanField(default=False)
    auth_needed_to_write = models.BooleanField(default=True)

    auth_opt_fb = models.BooleanField(default=True)
    auth_opt_tw = models.BooleanField(default=True)
    auth_opt_allow_3rdparty = models.BooleanField(default=True)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")


class Territory(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Territory")
        verbose_name_plural = _("Territories")


class Affinity(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Affinity")
        verbose_name_plural = _("Affinities")


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(
        max_length=2, choices=choices.GENDER_CHOICES, blank=True, null=True
    )
    year_of_birth = models.IntegerField(blank=True, null=True)
    territory = models.ForeignKey(
        Territory, on_delete=models.CASCADE, blank=True, null=True
    )
    affinity = models.ForeignKey(
        Affinity, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.id} {self.name}"

    class Meta:
        ordering = ["id", "affinity"]
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")


class PolisConversation(models.Model):
    # Define your fields here
    zid = models.BigIntegerField(primary_key=True)
    topic = models.TextField()
    description = models.TextField()
    upvotes = models.IntegerField()
    participant_count = models.IntegerField()
    is_anon = models.BooleanField()
    is_active = models.BooleanField()
    is_public = models.BooleanField()

    class Meta:
        db_table = "conversations"
        managed = False

    def save(self, *args, **kwargs):
        # Prevent any changes by overriding the save method
        pass

    def delete(self, *args, **kwargs):
        # Prevent deletion by overriding the delete method
        pass

    def __str__(self):
        return f"{self.zid} {self.topic}"


class PolisUser(models.Model):
    # Define your fields here
    uid = models.BigIntegerField(primary_key=True)
    hname = models.TextField()
    email = models.TextField()
    site_id = models.TextField()
    site_owner = models.BooleanField()

    class Meta:
        db_table = "users"
        managed = False

    def save(self, *args, **kwargs):
        # Prevent any changes by overriding the save method
        pass

    def delete(self, *args, **kwargs):
        # Prevent deletion by overriding the delete method
        pass

    def __str__(self):
        return f"{self.uid} {self.email}"


class PolisParticipant(models.Model):
    # Define your fields here
    pid = models.BigIntegerField(primary_key=True)
    zid = models.ForeignKey(
        PolisConversation, on_delete=models.CASCADE, db_column="zid"
    )
    uid = models.ForeignKey(PolisUser, on_delete=models.CASCADE, db_column="uid")
    vote_count = models.IntegerField()
    created = MillisField()
    last_interaction = MillisField()

    class Meta:
        db_table = "participants"
        managed = False

    def save(self, *args, **kwargs):
        # Prevent any changes by overriding the save method
        pass

    def delete(self, *args, **kwargs):
        # Prevent deletion by overriding the delete method
        pass

    def __str__(self):
        return f"{self.pid} {self.zid} {self.uid}"


class PolisXid(models.Model):
    # Define your fields here
    uid = models.BigIntegerField(primary_key=True, db_column="uid")

    xid = models.ForeignKey(Participant, on_delete=models.CASCADE, db_column="xid")
    x_profile_image_url = models.TextField()
    x_name = models.TextField()
    x_email = models.TextField()
    created = MillisField()
    modified = MillisField()

    def save(self, *args, **kwargs):
        # Prevent any changes by overriding the save method
        pass

    def delete(self, *args, **kwargs):
        # Prevent deletion by overriding the delete method
        pass

    def __str__(self):
        return f"{self.uid} {self.xid}"

    class Meta:
        db_table = "xids"
        managed = False
