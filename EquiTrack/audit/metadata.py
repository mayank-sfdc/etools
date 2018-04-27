from __future__ import absolute_import, division, print_function, unicode_literals

from rest_framework.metadata import SimpleMetadata

from attachments.metadata import ModelChoiceFieldMixin
from EquiTrack.metadata import FSMTransitionActionMetadataMixin
from permissions2.metadata import PermittedFSMTransitionActionMetadataMixin
from rest_extra.metadata import (
    CRUActionsMetadataMixin,
    ReadOnlyFieldWithChoicesMixin,
    SeparatedReadWriteFieldMetadata,
)
from permissions.metadata import PermissionsBasedMetadataMixin


class AuditBaseMetadata(
    ReadOnlyFieldWithChoicesMixin,
    ModelChoiceFieldMixin,
    SeparatedReadWriteFieldMetadata,
    CRUActionsMetadataMixin,
    SimpleMetadata
):
    pass


class AuditPermissionBasedMetadata(
    PermittedFSMTransitionActionMetadataMixin,
    PermissionsBasedMetadataMixin,
    AuditBaseMetadata
):
    def get_serializer_info(self, serializer):
        if serializer.instance:
            serializer.context['instance'] = serializer.instance
        return super(AuditPermissionBasedMetadata, self).get_serializer_info(serializer)
