from django.db import models
import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

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

def styleToHTML(styleDict):
    if not styleDict:
        return ""
    else:
        return "style=\"{}\"".format("; ".join((f"{k}: {v}" for (k,v) in styleDict.items())))

class DrugKey(models.Model):
    gtin = models.CharField(max_length=50)

    # funding
    registered_funding = models.TextField()
    nonregistered_funding = models.TextField(null=True)
    class Meta:
        unique_together = ('gtin', 'registered_funding', 'nonregistered_funding')

    def getData(self,attr,colour_diff=True):
        data = [getattr(x,attr) for x in Drug.objects.filter(key=self).order_by("date") if x.somethingHasChanged()]
        if not data:
            return
        prev = data[0]
        tableStyle = {"width":"100%", "height":"100%", "min-height": "100%", "display": "grid", "grid-auto-rows":"1fr"}
        html = f"<div {styleToHTML(tableStyle)}>"
        for (i,value) in enumerate(data):
            # style = tableStyle
            style={"display":"flex","flex-direction":"column","justify-content":"center"}
            if colour_diff and value != prev:
                style["background-color"]="cyan"
            if i != 0:
                style["border-top"] = "1px solid black"
            prev = value
            html += f"<div {styleToHTML(style)}>"
            html += str(value)
            html += "</div>"
        html += "</div>"
        return mark_safe(html)

    def getActiveSubstances(self):
        return self.getData("active_substance")

    def getDates(self):
        return self.getData("date",colour_diff=False)

    def getMedNames(self):
        return self.getData("med_name")

    def getMedForms(self):
        return self.getData("med_form")

    def getDoses(self):
        return self.getData("dose")

    def getCompanyNames(self):
        return self.getData("company_name")

    def getPackSizes(self):
        return self.getData("pack_size")

    def getLimitGroups(self):
        return self.getData("limit_group")

    def getPaymentLvls(self):
        return self.getData("payment_lvl")

    def getPatientPayments(self):
        return self.getData("patient_payment")

    def getOfficialPrices(self):
        return self.getData("official_price")

    def getWholesalePrices(self):
        return self.getData("wholesale_price")

    def getRetailPrices(self):
        return self.getData("retail_price")

    def getRefundLimits(self):
        return self.getData("refund_limit")


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

    def somethingHasChanged(self):
        return True