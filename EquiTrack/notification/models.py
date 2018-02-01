from __future__ import absolute_import

import json
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import six
from model_utils import Choices
from post_office import mail
from post_office.models import EmailTemplate

from utils.utils import make_dictionary_serializable

logger = logging.getLogger(__name__)


def validate_template_name(template_name):
    try:
        EmailTemplate.objects.get(name=template_name)
    except EmailTemplate.DoesNotExist:
        raise ValidationError("No such EmailTemplate: %s" % template_name)


def validate_notification_type(type_name):
    if type_name not in ('Email'):
        raise ValidationError("Notification type must be 'Email'")


@python_2_unicode_compatible
class Notification(models.Model):
    """
    Represents a notification instance from sender to recipients
    """

    TYPE_CHOICES = Choices(
        ('Email', 'Email'),
    )

    type = models.CharField(max_length=255, default='Email', validators=[validate_notification_type])
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    sender = GenericForeignKey('content_type', 'object_id')
    # from_address can be used as the notification from address if sender is
    # not a user with an email address.
    from_address = models.CharField(max_length=255, null=True, blank=True)
    recipients = ArrayField(
        models.CharField(max_length=255),
        blank=True,
    )
    cc = ArrayField(
        models.CharField(max_length=255),
        default=list,
        blank=True,
    )
    sent_recipients = ArrayField(
        models.CharField(max_length=255),
        default=list,
        blank=True,
    )
    template_name = models.CharField(max_length=255, validators=[validate_template_name], blank=True)
    template_data = JSONField(null=True, blank=True)
    sent_email = models.ForeignKey('post_office.Email', null=True, on_delete=models.CASCADE, blank=True)
    subject = models.TextField(default='', blank=True)
    text_message = models.TextField(default='', blank=True)
    html_message = models.TextField(default='', blank=True)

    def __str__(self):
        return u"{} Notification from {}: {}".format(self.type, self.sender, self.template_data)

    def __init__(self, *args, **kwargs):
        template_data = kwargs.pop('template_data', {})
        # Before trying to serialize template_data, we might need to make it serializable
        try:
            json.dumps(template_data)
        except TypeError:
            assert isinstance(template_data, dict)
            template_data = make_dictionary_serializable(template_data)
        kwargs['template_data'] = template_data
        super(Notification, self).__init__(*args, **kwargs)

    def clean(self):
        if (self.text_message or self.html_message) and self.template_name:
            raise ValidationError("Notification cannot have both a template name and a text_message or html_message")
        if not (self.text_message or self.html_message or self.template_name):
            raise ValidationError("Notification must have template name or text_message or html_message.")
        # We won't require there to be any recipients, since callers might find it easier to just call
        # this with whatever list of email addresses they have without having to first check whether they
        # have any addresses.
        # if not (len(self.cc) + len(self.recipients)):
        #     raise ValidationError("Notification must have at least one recipient or cc address.")

    def save(self, *args, **kwargs):
        super(Notification, self).save(*args, **kwargs)

    def send_notification(self):
        """
        Dispatch notification based on type.
        """
        if self.type == 'Email':
            self.send_mail()
        else:
            # for future notification methods
            pass

    def send_mail(self):
        User = get_user_model()

        if isinstance(self.sender, User):
            sender = self.sender.email
        elif self.from_address:
            sender = self.from_address
        else:
            sender = settings.DEFAULT_FROM_EMAIL

        if isinstance(self.template_data, six.string_types):
            template_data = json.loads(self.template_data)
        else:
            template_data = self.template_data

        try:
            email = mail.send(
                recipients=self.recipients,
                cc=self.cc,
                sender=sender,
                template=self.template_name,
                context=template_data,
                subject=self.subject,
                message=self.text_message,
                html_message=self.html_message,
            )
        except Exception:
            # log an exception, with traceback
            logger.exception('Failed to send mail.')
        else:
            self.sent_recipients = self.recipients + self.cc
            self.sent_email = email
            self.save()
