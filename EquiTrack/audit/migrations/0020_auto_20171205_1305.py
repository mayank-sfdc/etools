# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-12-05 13:05
from __future__ import unicode_literals

from django.db import migrations


def migrate_purchase_order(apps, schema_editor):
    TargetAuditorFirm = apps.get_model('purchase_order', 'AuditorFirm')
    TargetAuditorStaffMember = apps.get_model('purchase_order', 'AuditorStaffMember')
    TargetPurchaseOrder = apps.get_model('purchase_order', 'PurchaseOrder')
    TargetPurchaseOrderItem = apps.get_model('purchase_order', 'PurchaseOrderItem')

    SourceAuditorFirm = apps.get_model('audit', 'AuditorFirm')
    SourceAuditorStaffMember = apps.get_model('audit', 'AuditorStaffMember')
    SourcePurchaseOrder = apps.get_model('audit', 'PurchaseOrder')
    SourcePurchaseOrderItem = apps.get_model('audit', 'PurchaseOrderItem')

    firms = dict()
    for firm in SourceAuditorFirm.objects.all():
        if TargetAuditorFirm.objects.filter(vendor_number=firm.vendor_number).exists():
            firm = TargetAuditorFirm.objects.get(vendor_number=firm.vendor_number)

        else:
            firm .__class__ = TargetAuditorFirm
            firm.id = None
            firm.save()

        firms[firm.vendor_number] = firm

    for staff_member in SourceAuditorStaffMember.objects.select_related('auditor_firm'):
        if not TargetAuditorStaffMember.objects.filter(user_id=staff_member.user_id).exists():
            staff_member.__class__ = TargetAuditorStaffMember
            staff_member.id = None
            staff_member.auditor_firm = firms[staff_member.auditor_firm.vendor_number]
            staff_member.save()

    purchase_orders = dict()
    for purchase_order in SourcePurchaseOrder.objects.select_related('auditor_firm'):
        if TargetPurchaseOrder.objects.filter(order_number=purchase_order.order_number).exists():
            purchase_order = TargetPurchaseOrder.objects.get(order_number=purchase_order.order_number)

        else:
            purchase_order.__class__ = TargetPurchaseOrder
            purchase_order.id = None
            purchase_order.auditor_firm = firms[purchase_order.auditor_firm.vendor_number]
            purchase_order.save()

        purchase_orders[purchase_order.order_number] = purchase_order

    for po_item in SourcePurchaseOrderItem.objects.select_related('purchase_order'):
        if not TargetPurchaseOrderItem.objects.filter(
                purchase_order__order_number=po_item.purchase_order.order_number,
                number=po_item.number).exists():
            po_item.__class__ = TargetPurchaseOrderItem
            po_item.id = None
            po_item.purchase_order = purchase_orders[po_item.purchase_order.order_number]
            po_item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0019_auto_20171113_1150'),
        ('purchase_order', '0002_auto_20180111_0808'),
    ]

    operations = [
        migrations.RunPython(
            migrate_purchase_order,
            migrations.RunPython.noop,
        ),
    ]
