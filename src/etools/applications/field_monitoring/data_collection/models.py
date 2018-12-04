from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_fsm import transition, FSMField
from model_utils import Choices

from etools.applications.field_monitoring.shared.models import FMMethod
from etools.applications.field_monitoring.visits.models import Visit, VisitMethodType, VisitTaskLink, TaskCheckListItem, \
    FindingMixin


class StartedMethod(models.Model):
    STATUS_CHOICES = Choices(
        ('started', _('Started')),
        ('completed', _('Completed')),
    )

    visit = models.ForeignKey(Visit, related_name='started_methods', verbose_name=_('Visit'))
    method = models.ForeignKey(FMMethod, related_name='started_methods', verbose_name=_('Method'))
    method_type = models.ForeignKey(VisitMethodType, related_name='started_methods', verbose_name=_('Method Type'),
                                    blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='started_methods', verbose_name=_('Author'))
    status = FSMField(choices=STATUS_CHOICES, default=STATUS_CHOICES.started)

    class Meta:
        verbose_name = _('Started Method')
        verbose_name_plural = _('Started Methods')
        ordering = ('id',)

    def __str__(self):
        result = '{}: {}'.format(self.visit, self.method.name)

        if self.method_type:
            result += ' {}'.format(self.method_type.name)

        return result

    @transition(
        status, source=STATUS_CHOICES.started, target=STATUS_CHOICES.completed,
    )
    def complete(self):
        """
        Check if all required cp outputs are probed.
        """
        pass


class TaskData(models.Model):
    visit_task = models.ForeignKey(VisitTaskLink)
    started_method = models.ForeignKey(StartedMethod)
    is_probed = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Task Data')
        verbose_name_plural = _('Tasks Data')
        ordering = ('id',)

    def __str__(self):
        return 'TaskData for {}'.format(self.visit_task)


class CheckListItemValue(FindingMixin, models.Model):
    task_data = models.ForeignKey(TaskData)
    checklist_item = models.ForeignKey(TaskCheckListItem)

    class Meta:
        verbose_name = _('Checklist Item Value')
        verbose_name_plural = _('Checklists Item Values')
        ordering = ('id',)

    def __str__(self):
        return 'CheckListItemValue for {}'.format(self.task_data)