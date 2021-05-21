from django.db import models
import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings

class DrugManager(models.Manager):
    def set_diff_pk(self, drugs):
        for drug in drugs:
            drug.set_diff_pk()
    def get_changed(self):
        return self.raw(
            '''SELECT x.* FROM medsApp_drug AS x, medsApp_drug AS y
WHERE x.diff_pk_id IS NULL OR
(y.id=x.diff_pk_id AND
(y.active_substance!=x.active_substance OR
y.med_name!=x.med_name OR
y.med_form!=x.med_form OR
y.dose!=x.dose OR
y.pack_size!=x.pack_size OR
y.limit_group!=x.limit_group OR
y.payment_lvl!=x.payment_lvl OR
y.patient_payment!=x.patient_payment OR
y.official_price!=x.official_price OR
y.wholesale_price!=x.wholesale_price OR
y.retail_price!=x.retail_price OR
y.refund_limit!=x.refund_limit
)
);'''
        )

class Drug(models.Model):
    objects = DrugManager()

    diff_pk = models.ForeignKey('Drug', on_delete=models.SET_NULL, blank=True, null=True)

    gtin = models.CharField(max_length=50)

    # funding
    registered_funding = models.TextField()
    nonregistered_funding = models.TextField(null=True)

    # substance
    active_substance = models.CharField(max_length=100)

    date = models.DateTimeField()

    med_name = models.CharField(max_length=100)
    med_form = models.CharField(max_length=40, null=True)
    dose = models.CharField(max_length=40, null=True)

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

    def set_diff_pk(self):
        if not self.diff_pk:
            xd = Drug.objects.filter(gtin=self.gtin, registered_funding=self.registered_funding, nonregistered_funding=self.nonregistered_funding).exclude(pk=self.pk)
            self.diff_pk = xd[0] if xd else None
            self.save()

    @property
    def diff_active_substance(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).active_substance
            return tmp if tmp == self.active_substance else '{0} | {1}'.format(self.active_substance, tmp)
        return self.active_substance + ' | none'

    @property
    def diff_date(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).date
            if (not tmp):
                print(self)
                print('puste')
            return tmp if tmp == self.date else '{0} | {1}'.format(self.date, tmp)
        return self.date + ' | none '

    @property
    def diff_med_name(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).med_name
            return tmp if tmp == self.med_name else '{0} | {1}'.format(self.med_name, tmp)
        return self.med_name + ' | none'

    @property
    def diff_med_form(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).med_form
            return tmp if tmp == self.med_form else '{0} | {1}'.format(self.med_form, tmp)
        return self.med_form + ' | none'

    @property
    def diff_dose(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).dose
            return tmp if tmp == self.dose else '{0} | {1}'.format(self.dose, tmp)
        return self.dose + ' | none'

    @property
    def diff_pack_size(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).pack_size
            return tmp if tmp == self.pack_size else '{0} | {1}'.format(self.pack_size, tmp)
        return self.pack_size + ' | none'

    @property
    def diff_limit_group(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).limit_group
            return tmp if tmp == self.limit_group else '{0} | {1}'.format(self.limit_group, tmp)
        return self.limit_group + ' | none'

    @property
    def diff_payment_lvl(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).payment_lvl
            return tmp if tmp == self.payment_lvl else '{0} | {1}'.format(self.payment_lvl, tmp)
        return self.payment_lvl + ' | none'

    @property
    def diff_patient_payment(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).patient_payment
            return tmp if tmp == self.patient_payment else '{0} | {1}'.format(self.patient_payment, tmp)
        return self.patient_payment + ' | none'

    @property
    def diff_official_price(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).official_price
            return tmp if tmp == self.official_price else '{0} | {1}'.format(self.official_price, tmp)
        return self.official_price + ' | none'

    @property
    def diff_wholesale_price(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).wholesale_price
            return tmp if tmp == self.wholesale_price else '{0} | {1}'.format(self.wholesale_price, tmp)
        return self.wholesale_price + ' | none'

    @property
    def diff_retail_price(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).retail_price
            return tmp if tmp == self.retail_price else '{0} | {1}'.format(self.retail_price, tmp)
        return self.retail_price + ' | none'

    @property
    def diff_refund_limit(self):
        if self.diff_pk:
            tmp = Drug.objects.get(pk=self.diff_pk.pk).refund_limit
            return tmp if tmp == self.refund_limit else '{0} | {1}'.format(self.refund_limit, tmp)
        return self.refund_limit + ' | none'
