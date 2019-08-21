from etools_validator.exceptions import StateValidationError
from etools_validator.utils import check_required_fields, check_rigid_fields
from etools_validator.validation import CompleteValidation

from etools.applications.psea.permissions import AssessmentPermissions


class AssessmentValid(CompleteValidation):
    VALIDATION_CLASS = 'psea.Assessment'
    PERMISSIONS_CLASS = AssessmentPermissions
    BASIC_VALIDATIONS = []
    VALID_ERRORS = {}

    def check_required_fields(self, assessment):
        required_fields = [
            f for f in self.permissions['required']
            if self.permissions['required'][f] is True
        ]
        required_valid, field = check_required_fields(
            assessment,
            required_fields,
        )
        if not required_valid:
            raise StateValidationError(
                ['Required fields not completed in {}: {}'.format(
                    assessment.status,
                    field,
                )]
            )

    def check_rigid_fields(self, assessment, related=False):
        # this can be set if running in a task and old_instance is not set
        if self.disable_rigid_check:
            return
        rigid_fields = [
            f for f in self.permissions['edit']
            if self.permissions['edit'][f] is False
        ]
        rigid_valid, field = check_rigid_fields(
            assessment,
            rigid_fields,
            related=related,
        )
        if not rigid_valid:
            raise StateValidationError(
                ['Cannot change fields while in {}: {}'.format(
                    assessment.status,
                    field,
                )]
            )

    def state_draft_valid(self, assessment, user=None):
        self.check_required_fields(assessment)
        self.check_rigid_fields(assessment, related=True)
        return True

    def state_signed_valid(self, assessment, user=None):
        self.check_required_fields(assessment)
        self.check_rigid_fields(assessment, related=True)
        return True

    def state_ended_valid(self, assessment, user=None):
        self.check_required_fields(assessment)
        self.check_rigid_fields(assessment, related=True)
        # today = date.today()
        # if not today > agreement.end:
        #     raise StateValidationError([_('Today is not after the end date')])
        return True
