import django_tables2 as tables
from .models import *
import django_filters as filters
import django_filters.views

def key_cols(s):
    s -= {'diff_id', 'diff_diff_pk', 'diff_gtin', 'diff_registered_funding', 'diff_nonregistered_funding'}
    s |= {'gtin', 'registered_funding', 'nonregistered_funding'}
    return s

class DrugTable(tables.Table):
    diff_date = tables.Column(accessor='diff_date', verbose_name='Date')
    diff_active_substance = tables.Column(accessor='diff_active_substance', verbose_name='Active substance')
    diff_payment_lvl = tables.Column(accessor='diff_payment_lvl', verbose_name='Payement level')
    diff_official_price = tables.Column(accessor='diff_official_price', verbose_name='Official price')
    diff_limit_group = tables.Column(accessor='diff_limit_group', verbose_name='Limit group')
    diff_med_form = tables.Column(accessor='diff_med_form', verbose_name='Medicine form')
    diff_dose = tables.Column(accessor='diff_dose', verbose_name='Dose')
    diff_med_name = tables.Column(accessor='diff_med_name', verbose_name='Medicine name')
    diff_retail_price = tables.Column(accessor='diff_retail_price', verbose_name='Retail price')
    diff_pack_size = tables.Column(accessor='diff_pack_size', verbose_name='Pack size')
    diff_refund_limit = tables.Column(accessor='diff_refund_limit', verbose_name='Refund limit')
    diff_patient_payment = tables.Column(accessor='diff_patient_payment', verbose_name='Patient payment')
    diff_wholesale_price = tables.Column(accessor='diff_wholesale_price', verbose_name='Wholesale price')
    class Meta:
        model = Drug
        attrs = {'class': 'table'}
        fields = key_cols({'diff_' + f.name for f in Drug._meta.fields})
        sequence = (
            'diff_date',
            'gtin',
            'diff_med_name',
            'registered_funding',
            'nonregistered_funding',
            'diff_active_substance',
            'diff_med_form',
            'diff_dose',
            'diff_pack_size',
            'diff_limit_group',
            'diff_official_price',
            'diff_wholesale_price',
            'diff_retail_price',
            'diff_refund_limit',
            'diff_payment_lvl',
            'diff_patient_payment',
        )

# class DrugFilter(tables.SingleTableMixin,filters.views.FilterView):
#     table_class = DrugTable
#     model = Drug


class DrugFilterSet(filters.FilterSet):
    class Meta:
        model = Drug
        fields = {
            "gtin": ["contains"],
            "dose": ["contains"],
            "company_name": ["contains"],
        }
