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

    med_name = filters.CharFilter(field_name="med_name",method="multifilter",label="Medication name",lookup_expr="contains")
    dosage = filters.CharFilter(field_name="does",method="multifilter",label="Dosage",lookup_expr="contains")
    company_name = filters.CharFilter(field_name="company_name",method="multifilter",label="Company name",lookup_expr="contains")

    def multifilter(self,queryset, name, value):
        ids = set(x.key.id for x in Drug.objects.filter(**{name + "__contains":value}))
        return queryset.filter(id__in=ids)

    class Meta:
        model = DrugKey
        # fields = {
        #     "med_name": ["contains"],
        #     "company_name": ["contains"],
        #     "limit_group": ["contains"],
        #     "active_substance": ["contains"]
        # }
        fields = {
            "gtin": ["contains"]
        }

defaultColumnArgs = {
"attrs":{"td":{"style":"height:0"}},
    "orderable":False
}

class DrugKeyTable(tables.Table):
    activeSubstances = tables.TemplateColumn("{{ record.getActiveSubstances }}",**defaultColumnArgs,verbose_name='Active substances')
    dates = tables.TemplateColumn("{{ record.getDates }}",**defaultColumnArgs,verbose_name='Dates')
    medNames = tables.TemplateColumn("{{ record.getMedNames }}",**defaultColumnArgs,verbose_name='Medicine names')
    medForms = tables.TemplateColumn("{{ record.getMedForms }}",**defaultColumnArgs,verbose_name='Medicine forms')
    doses = tables.TemplateColumn("{{ record.getDoses }}",**defaultColumnArgs,verbose_name='Dosages')
    companyNames = tables.TemplateColumn("{{ record.getCompanyNames }}",**defaultColumnArgs,verbose_name='Company names')
    packSizes = tables.TemplateColumn("{{ record.getPackSizes }}",**defaultColumnArgs,verbose_name='Pack sizes')
    limitGroups = tables.TemplateColumn("{{ record.getLimitGroups }}",**defaultColumnArgs,verbose_name='Limit groups')
    paymentLvls = tables.TemplateColumn("{{ record.getPaymentLvls }}",**defaultColumnArgs,verbose_name='Payment lvls')
    patientPayments = tables.TemplateColumn("{{ record.getPatientPayments }}",**defaultColumnArgs,verbose_name='Patient payments')
    officialPrices = tables.TemplateColumn("{{ record.getOfficialPrices }}",**defaultColumnArgs,verbose_name='Official prices')
    wholesalePrices = tables.TemplateColumn("{{ record.getWholesalePrices }}",**defaultColumnArgs,verbose_name='Wholesale prices')
    retailPrices = tables.TemplateColumn("{{ record.getRetailPrices }}",**defaultColumnArgs,verbose_name='Retail prices')
    refundLimits = tables.TemplateColumn("{{ record.getRefundLimits }}",**defaultColumnArgs,verbose_name='Refund limits')


    class Meta:
        model = DrugKey
        attrs = {'class': 'table'}
        row_attrs = {
            'class': 'drugRow',
            'id': lambda record: record.id
        }
        # fields = sequence = ('gtin', 'registered_funding', 'nonregistered_funding')
