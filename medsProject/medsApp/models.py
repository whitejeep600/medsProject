from django.db import models
import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings

class DrugManager(models.Manager):
    def set_companies(self, path):
        file = open(path)
        line = file.readline()
        while line != "":
            tokens = line.split('|')
            gtin = tokens[0]
            company_name = tokens[1]
            for drug in Drug.objects.filter(gtin=gtin):
                drug.company_name = company_name
                drug.save()
            line = file.readline()
        file.close()


class DrugKey(models.Model):
    gtin = models.CharField(max_length=50)

    # funding
    registered_funding = models.TextField()
    nonregistered_funding = models.TextField(null=True)
    class Meta:
        unique_together = ('gtin', 'registered_funding', 'nonregistered_funding')

class Drug(models.Model):
    objects = DrugManager()

    key = models.ForeignKey('DrugKey', on_delete=models.CASCADE, blank=True)

    # substance
    active_substance = models.CharField(max_length=100)

    date = models.DateTimeField()

    med_name = models.CharField(max_length=100)
    med_form = models.CharField(max_length=40, null=True)
    dose = models.CharField(max_length=40, null=True)
    company_name = models.CharField(max_length=40, null=True)
    pack_size = models.CharField(max_length=50)

    limit_group = models.TextField(null=True)

    class PaymentType(models.TextChoices):
        SMALLER_PRC = '50%', _('50 %')
        BIGGER_PRC = '30%', _('30 %')
        CONST = 'ryczałt', _('Ryczałt')
        FREE = 'bezpłatny do limitu', _('Bezpłatny do limitu')

    payment_lvl = models.CharField(
        max_length=20,
        choices=PaymentType.choices, 
    )
    
    patient_payment = models.DecimalField(decimal_places=2, max_digits=8)

    official_price = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    wholesale_price = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    retail_price = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    refund_limit = models.DecimalField(decimal_places=2, max_digits=8, null=True)
