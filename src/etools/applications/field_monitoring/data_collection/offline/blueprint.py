from django.db import connection
from django.utils.translation import ugettext_lazy as _

from unicef_attachments.models import FileType

from etools.applications.field_monitoring.fm_settings.models import Method, Question
from etools.applications.field_monitoring.planning.models import MonitoringActivity
from etools.applications.offline.blueprint import Blueprint
from etools.applications.offline.fields import (
    BooleanField,
    ChoiceField,
    FloatField,
    Group,
    TextField,
    UploadedFileField,
)
from etools.applications.offline.fields.choices import LocalPairsOptions

answer_type_to_field_mapping = {
    Question.ANSWER_TYPES.text: TextField,
    Question.ANSWER_TYPES.number: FloatField,
    Question.ANSWER_TYPES.bool: BooleanField,  # todo: we need to check if frontend use booleans instead of text
    Question.ANSWER_TYPES.likert_scale: TextField,
}


def get_blueprint_for_activity_and_method(activity: MonitoringActivity, method: Method) -> Blueprint:
    country_code = connection.tenant.country_short_code or ''

    blueprint = Blueprint(
        f'fm_{country_code}_{activity.id}_{method.id}',
        '{} for {}'.format(method.name, activity.reference_number),
    )
    if method.use_information_source:
        blueprint.add(TextField('information_source', label=_('Source of Information'), extra={'type': ['wide']}))

    for relation, level in activity.RELATIONS_MAPPING:
        level_block = Group(level, extra={'type': ['abstract']})

        for target in getattr(activity, relation).all():
            target_questions = activity.questions.filter(
                **{Question.get_target_relation_name(level): target},
                is_enabled=True, question__methods=method
            )
            if not target_questions.exists():
                continue

            target_block = Group(
                str(target.id),
                TextField(
                    'overall', label=_('Overall Finding'), extra={'type': ['wide', 'additional']}, required=False
                ),
                Group(
                    'attachments',
                    UploadedFileField('attachment'),
                    ChoiceField('file_type', options_key='target_attachments_file_types'),
                    required=False, repeatable=True
                ),
                title=str(target)
            )
            questions_block = Group('questions', extra={'type': ['abstract']})
            target_block.add(questions_block)
            for question in target_questions.distinct():
                if question.question.answer_type in [
                    Question.ANSWER_TYPES.bool,
                    Question.ANSWER_TYPES.likert_scale
                ]:
                    options_key = 'question_{}'.format(question.question.id)
                    blueprint.metadata.options[options_key] = LocalPairsOptions(
                        question.question.options.values_list('value', 'label')
                    )
                else:
                    options_key = None

                questions_block.add(
                    answer_type_to_field_mapping[question.question.answer_type](
                        str(question.question.id),
                        label=question.question.text,
                        options_key=options_key,
                        help_text=question.specific_details
                    )
                )
            level_block.add(target_block)

        if level_block.children:
            blueprint.add(level_block)

    blueprint.metadata.options['target_attachments_file_types'] = LocalPairsOptions(
        FileType.objects.filter(code='fm_common').values_list('id', 'label')
    )

    return blueprint


def get_monitoring_activity_blueprints(activity: MonitoringActivity):
    for method in Method.objects.filter(
        pk__in=activity.questions.filter(
            is_enabled=True
        ).values_list('question__methods', flat=True)
    ):
        yield get_blueprint_for_activity_and_method(activity, method)