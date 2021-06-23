import django_tables2 as tables
from .models import *
import django_filters as filters
import django_filters.views


def key_cols(s):
    s -= {'diff_id', 'diff_diff_pk', 'diff_gtin', 'diff_registered_funding', 'diff_nonregistered_funding',
          'diff_company_name', 'diff_last_changed'}
    s |= {'gtin', 'registered_funding', 'nonregistered_funding'}
    return s


class DrugTable(tables.Table):
    diff_date = tables.TemplateColumn("{{ record.diff_date | linebreaksbr }}", verbose_name='Date')
    diff_active_substance = tables.TemplateColumn("{{record.diff_active_substance|linebreaksbr}}",
                                                  verbose_name='Active substance')
    diff_payment_lvl = tables.TemplateColumn("{{record.diff_payment_lvl|linebreaksbr}}", verbose_name='Payement level')
    diff_official_price = tables.TemplateColumn("{{record.diff_official_price|linebreaksbr}}",
                                                verbose_name='Official price')
    diff_limit_group = tables.TemplateColumn("{{record.diff_limit_group|linebreaksbr}}", verbose_name='Limit group')
    diff_med_form = tables.TemplateColumn("{{record.diff_med_form|linebreaksbr}}", verbose_name='Medicine form')
    diff_dose = tables.TemplateColumn("{{record.diff_dose|linebreaksbr}}", verbose_name='Dose')
    diff_med_name = tables.TemplateColumn("{{record.diff_med_name|linebreaksbr}}", verbose_name='Medicine name')
    diff_retail_price = tables.TemplateColumn("{{record.diff_retail_price|linebreaksbr}}", verbose_name='Retail price')
    diff_pack_size = tables.TemplateColumn("{{record.diff_pack_size|linebreaksbr}}", verbose_name='Pack size')
    diff_refund_limit = tables.TemplateColumn("{{record.diff_refund_limit|linebreaksbr}}", verbose_name='Refund limit')
    diff_patient_payment = tables.TemplateColumn("{{record.diff_patient_payment|linebreaksbr}}",
                                                 verbose_name='Patient payment')
    diff_wholesale_price = tables.TemplateColumn("{{record.diff_wholesale_price|linebreaksbr}}",
                                                 verbose_name='Wholesale price')

    class Meta:
        model = Drug
        attrs = {'class': 'table'}
        row_attrs = {}


# class DrugFilter(tables.SingleTableMixin,filters.views.FilterView):
#     table_class = DrugTable
#     model = Drug


class DrugFilterSet(filters.FilterSet):
    class Meta:
        model = Drug
        fields = {
            "med_name": ["contains"],
            "company_name": ["contains"],
            "limit_group": ["contains"],
            "active_substance": ["contains"]
        }


class DrugKeyTable(tables.Table):
    drugData = tables.TemplateColumn("{% load render_table from django_tables2 %}{% load bootstrap3 %}{% render_table record.getData 'django_tables2/bootstrap.html' %}")

    class Meta:
        model = DrugKey
        attrs = {'class': 'table'}
        row_attrs = {
            'class': 'drugRow'
        }
        fields = sequence = ('gtin', 'registered_funding', 'nonregistered_funding')


DrugKey.getData = lambda self: DrugTable(Drug.objects.filter(key=self))
