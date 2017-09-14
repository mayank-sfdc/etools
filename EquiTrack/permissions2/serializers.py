from __future__ import absolute_import

from rest_framework import serializers
from rest_framework.utils import model_meta
from rest_framework_recursive.fields import RecursiveField

from utils.common.serializers.fields import SeparatedReadWriteField
from .utils import collect_parent_models
from .models import Permission


class PermissionsBasedSerializerMixin(object):
    def _collect_permissions_targets(self):
        """
        Collect permissions targets based on serializer's model and field name from full serializers tree.
        :return:
        """
        targets = list()

        # Breath-first search
        queue = [self.root]
        while queue:
            node = queue.pop(0)

            if isinstance(node, serializers.ListSerializer):
                queue.append(node.child)
                continue

            if isinstance(node, RecursiveField):
                node_fields = []
            else:
                node_fields = node.fields.values()

            for field in node_fields:
                if isinstance(node, PermissionsBasedSerializerMixin):
                    related_models = collect_parent_models(node.Meta.model)
                    targets.extend(map(
                        lambda model: Permission.get_target(model, field),
                        related_models
                    ))

                if isinstance(field, SeparatedReadWriteField):
                    if isinstance(field.read_field, serializers.BaseSerializer):
                        queue.append(field.read_field)
                    if isinstance(field.write_field, serializers.BaseSerializer):
                        queue.append(field.write_field)

                if isinstance(field, serializers.BaseSerializer):
                    queue.append(field)

        return targets

    def _collect_permissions(self):
        """
        Collect permission objects.
        :return:
        """
        targets = self._collect_permissions_targets()
        perms = self._get_permissions_queryset(targets)
        context = self._get_permission_context()
        if context:
            perms = perms.filter_by_context(context)
        return perms

    def _get_permissions_queryset(self, targets):
        return Permission.objects.filter_by_targets(targets)

    def _get_permission_context(self):
        return self.context.get('permission_context', [])

    @property
    def permissions(self):
        """
        Return permission objects related to current serializer.
        :return:
        """
        if not hasattr(self.root, '_permissions'):
            self.root._permissions = list(self._collect_permissions())

        permissions = self.root._permissions
        related_models = tuple(map(lambda model: Permission.get_target(model, ''),
                                   collect_parent_models(self.Meta.model)))
        permissions = filter(lambda p: p.target.startswith(related_models), permissions)

        context = set(self._get_permission_context())
        permissions = filter(lambda p: set(p.condition).issubset(context), permissions)

        return permissions

    def _filter_fields_by_permissions(self, fields, permission):
        model = self.Meta.model
        targets_map = {Permission.get_target(model, field): field for field in fields}

        pk_fields = []
        pk_target = Permission.get_target(model, 'pk')
        if pk_target in targets_map:
            pk_fields.append(targets_map.pop(pk_target))

        pk_field = model_meta.get_field_info(model).pk
        pk_target = Permission.get_target(model, pk_field)
        if pk_target in targets_map:
            pk_fields.append(targets_map.pop(pk_target))

        allowed_targets = Permission.apply_permissions(self.permissions, targets_map.keys(), permission)

        allowed_fields = map(lambda target: targets_map[target], allowed_targets)

        if allowed_fields:
            allowed_fields.extend(pk_fields)

        return allowed_fields

    @property
    def _writable_fields(self):
        fields = super(PermissionsBasedSerializerMixin, self)._writable_fields

        return self._filter_fields_by_permissions(fields, Permission.PERMISSIONS.edit)

    @property
    def _readable_fields(self):
        fields = super(PermissionsBasedSerializerMixin, self)._readable_fields

        return self._filter_fields_by_permissions(fields, Permission.PERMISSIONS.view)
