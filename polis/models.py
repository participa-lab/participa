import datetime
import hashlib
import logging
import uuid

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from polis import choices

logger = logging.getLogger(__name__)


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
    name = models.CharField(_("Nombre"), max_length=200)
    url = models.CharField(max_length=200)
    site_id = models.CharField(_("Polis Site Id"), max_length=200)

    def __str__(self):
        return f"{self.id} {self.name}"

    class Meta:
        verbose_name = _("Instancia")
        verbose_name_plural = _("Instancias")


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(_("Tema"), max_length=200)
    slug = models.SlugField(_("Slug"), default="", null=False)
    description = models.TextField(_("Descripción"))

    start_date = models.DateTimeField(_("Fecha de inicio"))
    end_date = models.DateTimeField(_("Fecha de finalización"))
    instance = models.ForeignKey(
        Instance, on_delete=models.CASCADE, verbose_name=_("Instancia")
    )

    border = models.CharField(
        _("Border"), max_length=200, blank=True, null=True, default="0px solid #ccc"
    )
    border_radius = models.CharField(
        max_length=200, blank=True, null=True, default="4px"
    )
    padding = models.CharField(
        _("Iframe Padding"), max_length=200, blank=True, null=True, default="4px"
    )
    height = models.CharField(
        _("Iframe Height"), max_length=200, blank=True, null=True, default="400"
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

    color_primary = models.CharField(
        _("Primary color"), max_length=200, blank=True, null=True
    )
    color_secondary = models.CharField(
        _("Secondary color"), max_length=200, blank=True, null=True
    )
    show_in_list = models.BooleanField(_("Show in list"), default=False)

    def __str__(self):
        return self.topic

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sync_with_polis()

    def sync_with_polis(self):
        try:
            polis_conversation = PolisConversation.objects.filter(
                zid=self.get_polis_conversation_zid()
            ).first()
            if polis_conversation:
                polis_conversation.topic = self.topic
                polis_conversation.description = self.description
                polis_conversation.style_btn = self.color_primary
                polis_conversation.save()
        except Exception as e:
            logger.error(f"Error syncing with polis: {e}", exc_info=True)

    def get_polis_conversation_zid(self):
        polis_page_id = PolisPageId.objects.get(page_id=self.slug)
        return polis_page_id.zid

    def get_report_url(self):
        url = None
        try:
            polis_report = PolisReport.objects.get(
                zid=self.get_polis_conversation_zid()
            )
            url = self.instance.url + "/report/" + polis_report.report_id
        except Exception:
            pass

        return url

    @property
    def participant_count(self):
        return PolisConversation.objects.get(
            zid=self.get_polis_conversation_zid()
        ).participant_count

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
    name = models.CharField(_("Nombre"), max_length=200, blank=True, null=True)
    nick_name = models.CharField(_("Apodo"), max_length=200, blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    gender = models.CharField(
        _("Gender"), max_length=2, choices=choices.GENDER_CHOICES, blank=True, null=True
    )
    year_of_birth = models.IntegerField(_("Año de nacimiento"), blank=True, null=True)
    territory = models.ForeignKey(
        Territory,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Territorio"),
    )
    affinity = models.ForeignKey(
        Affinity,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Afiliación"),
    )

    def __str__(self):
        return f"{self.id} {self.name} {self.nick_name}"

    @property
    def some_name(self):
        return self.name or self.nick_name

    def refresh_xid_metadata(self):
        id_str = "{}".format(self.id)
        polis_xid = PolisXid.objects.filter(xid=id_str).first()
        if polis_xid:
            logger.info(
                f"Assigning participant {self} to PolisXid metadata {polis_xid}"
            )
            polis_xid.update_with_participant(self)
        else:
            logger.error(f"PolisXid not found for participant {self.id}")

    def assign_user(self, user):
        if not user or not user.is_authenticated:
            logger.error(f"assign_user: User {user} is not authenticated")
            return None

        user = User.objects.get(pk=user.pk)

        with transaction.atomic():
            preferred_avatar_size_pixels = 256

            email = user.email
            picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
                hashlib.md5(user.email.encode("UTF-8")).hexdigest(),
                preferred_avatar_size_pixels,
            )

            social_account = SocialAccount.objects.filter(user=user).first()
            logger.info(f"assign_user: social_account {social_account.provider}")

            try:
                # Extract first / last names from social nets and store on User record
                if social_account.provider.lower() == "twitter":
                    name = social_account.extra_data["name"]
                    name_parts = name.split()
                    if len(name_parts) > 0:
                        user.first_name = name_parts[0]
                    if len(name_parts) > 1:
                        user.last_name = name_parts[1]
                    picture_url = social_account.extra_data["profile_image_url"]
                    logger.info(
                        f"assign_user: Twitter user name {name}, picture_url {picture_url}"
                    )

                if social_account.provider.lower() == "facebook":
                    f_name = social_account.extra_data["first_name"]
                    l_name = social_account.extra_data["last_name"]
                    if f_name:
                        user.first_name = f_name
                    if l_name:
                        user.last_name = l_name

                    picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
                        social_account.uid, preferred_avatar_size_pixels
                    )
                    logger.info(
                        f"assign_user: Facebook user name {f_name} {l_name}, picture_url {picture_url}"
                    )

                if social_account.provider.lower() == "google":
                    f_name = social_account.extra_data["given_name"]
                    l_name = social_account.extra_data["family_name"]
                    if f_name:
                        user.first_name = f_name
                    if l_name:
                        user.last_name = l_name
                    picture_url = social_account.extra_data["picture"]
                    email = social_account.extra_data["email"]
                    logger.info(
                        f"assign_user: Google user name {f_name} {l_name}, picture_url {picture_url}, email {email}"
                    )

                if social_account.provider.lower() == "telegram":
                    f_name = social_account.extra_data["first_name"]
                    l_name = social_account.extra_data.get("last_name", "")
                    if f_name:
                        user.first_name = f_name
                    if l_name:
                        user.last_name = l_name
                    picture_url = social_account.extra_data["photo_url"]
                    logger.info(
                        f"assign_user: Telegram user name {f_name} {l_name}, picture_url {picture_url}, email {email}"
                    )

            except Exception as e:
                logger.error(f"assign_user: Error assigning user: {e}")

            logger.info(f"assign_user: Updating participant {self} with user {user}")
            self.user = user
            self.avatar_url = picture_url
            self.name = user.get_full_name()
            self.email = email
            self.save()

            user.save()

            self.refresh_xid_metadata()

        return self

    def merge(self, participant):
        self.nick_name = participant.nick_name
        self.gender = participant.gender
        self.year_of_birth = participant.year_of_birth
        self.territory = participant.territory
        self.affinity = participant.affinity
        self.email = participant.email if participant.email else self.email
        self.avatar_url = (
            participant.avatar_url if participant.avatar_url else self.avatar_url
        )
        self.save()

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
    style_btn = models.TextField()

    class Meta:
        db_table = "conversations"
        managed = False

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

    xid = models.TextField()
    x_profile_image_url = models.TextField()
    x_name = models.TextField()
    x_email = models.TextField()
    created = MillisField()
    modified = MillisField()

    def update_with_participant(self, participant):
        self.x_name = participant.some_name
        self.x_email = participant.email
        self.x_profile_image_url = participant.avatar_url
        self.save()

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
