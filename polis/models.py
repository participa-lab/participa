import datetime
import uuid

from django.contrib.auth.models import User
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
    name = models.CharField(_("Name"), max_length=200)
    url = models.CharField(max_length=200)
    site_id = models.CharField(_("Polis Site Id"), max_length=200)

    def __str__(self):
        return f"{self.id} {self.name}"

    class Meta:
        verbose_name = _("Instance")
        verbose_name_plural = _("Instances")


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(_("Topic"), max_length=200)
    slug = models.SlugField(_("Slug"), default="", null=False)
    description = models.TextField(_("Description"))

    start_date = models.DateTimeField(_("Start date"))
    end_date = models.DateTimeField(_("Start date"))
    instance = models.ForeignKey(
        Instance, on_delete=models.CASCADE, verbose_name=_("Instance")
    )

    border = models.CharField(
        _("Border"), max_length=200, blank=True, null=True, default="1px solid #ccc"
    )
    border_radius = models.CharField(
        max_length=200, blank=True, null=True, default="4px"
    )
    padding = models.CharField(
        _("Iframe Padding"), max_length=200, blank=True, null=True, default="4px"
    )
    height = models.CharField(
        _("Iframe Height"), max_length=200, blank=True, null=True, default="930"
    )
    ui_language = models.CharField(
        _("Iframe UI Languaje"), max_length=200, blank=True, null=True
    )
    dwok = models.CharField(_("Iframe Border"), max_length=200, blank=True, null=True)

    show_visualization = models.BooleanField(_("Show Visualization"), default=True)
    show_share = models.BooleanField(_("Show Share"), default=True)
    bg_white = models.BooleanField(_("Background White"), default=True)

    auth_needed_to_vote = models.BooleanField(
        _("Authentication needed to vote"), default=False
    )
    auth_needed_to_write = models.BooleanField(
        _("Authentication needed to write"), default=True
    )

    auth_opt_fb = models.BooleanField(_("Show Facebook Authentication"), default=True)
    auth_opt_tw = models.BooleanField(_("Show Twitter Authentication"), default=True)
    auth_opt_allow_3rdparty = models.BooleanField(
        _("Show 3rd Party Authentication"), default=True
    )

    show_footer = models.BooleanField(_("Show footer"), default=False)
    show_help = models.BooleanField(_("Show help text"), default=False)
    show_description = models.BooleanField(_("Show description"), default=True)
    show_topic = models.BooleanField(_("Show topic"), default=True)
    subscribe_type = models.CharField(
        _("Show subscribe type"),
        max_length=1,
        blank=True,
        null=True,
        choices=choices.SUSCRIBE_CHOICES,
    )

    def __str__(self):
        return self.topic

    def get_report_url(self):
        url = None
        try:
            polis_page_id = PolisPageId.objects.get(page_id=self.slug)
            polis_report = PolisReport.objects.get(zid=polis_page_id.zid)
            url = self.instance.url + "/report/" + polis_report.report_id
        except Exception:
            pass

        return url

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")


class Territory(models.Model):
    name = models.CharField(_("Name"), max_length=200, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Territory")
        verbose_name_plural = _("Territories")


class Affinity(models.Model):
    name = models.CharField(_("Name"), max_length=200, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Affinity")
        verbose_name_plural = _("Affinities")


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        verbose_name=_("user"),
        related_name="participant",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    avatar_url = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(_("Name"), max_length=200, blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    gender = models.CharField(
        _("Gender"), max_length=2, choices=choices.GENDER_CHOICES, blank=True, null=True
    )
    year_of_birth = models.IntegerField(_("Year of Birth"), blank=True, null=True)
    territory = models.ForeignKey(
        Territory,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Territory"),
    )
    affinity = models.ForeignKey(
        Affinity,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Affinity"),
    )

    def __str__(self):
        return f"{self.id} {self.name}"

    class Meta:
        ordering = ["id", "affinity"]
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")


class PolisPageId(models.Model):
    zid = models.BigIntegerField(primary_key=True)
    page_id = models.TextField()
    site_id = models.TextField()

    class Meta:
        db_table = "page_ids"
        managed = False

    def save(self, *args, **kwargs):
        # Prevent any changes by overriding the save method
        pass

    def delete(self, *args, **kwargs):
        # Prevent deletion by overriding the delete method
        pass

    def __str__(self):
        return f"{self.zid}"


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


class PolisReport(models.Model):
    rid = models.BigIntegerField(primary_key=True)
    report_id = models.TextField()
    zid = models.ForeignKey(
        PolisConversation, on_delete=models.CASCADE, db_column="zid"
    )
    report_id = models.TextField()

    class Meta:
        db_table = "reports"
        managed = False

    def save(self, *args, **kwargs):
        # Prevent any changes by overriding the save method
        pass

    def delete(self, *args, **kwargs):
        # Prevent deletion by overriding the delete method
        pass

    def __str__(self):
        return f"{self.zid}"
