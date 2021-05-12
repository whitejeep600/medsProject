from django.db import models
import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings


class Drug(models.Model):
    gtin = models.CharField(max_length=50, null=True)

    # funding
    registered_funding = models.TextField(null=True)
    nonregistered_funding = models.TextField(null=True)

    # substance
    active_substance = models.CharField(max_length=100, null=True)

    MED = models.CharField(max_length=100, null=True)

    # TODO
    # Add some null constraints maybe
    # date = models.DateField()
    # med_name = models.CharField(max_length=100)
    # med_form = models.CharField(max_length=40)
    # dose = models.CharField(max_length=40)

    pack_size = models.CharField(max_length=50, null=True)

    limit_group = models.TextField(null=True)

    class PaymentType(models.TextChoices):
        SMALLER_PRC = '50', _('50 %')
        BIGGER_PRC = '30', _('30 %')
        CONST = 'ryczalt', _('Ryczałt')
        FREE = 'free', _('Bezpłatnie')

    payment_lvl = models.CharField(
        max_length=7,
        choices=PaymentType.choices, 
        null=True
    )

    patient_payment = models.DecimalField(decimal_places=2, max_digits=8, null=True)

    official_price = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    wholesale_price = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    retail_price = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    refund_limit = models.DecimalField(decimal_places=2, max_digits=8, null=True)
