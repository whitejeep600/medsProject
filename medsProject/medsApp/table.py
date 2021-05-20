import django_tables2 as tables
from .models import *
import django_filters as filters
import django_filters.views


class DrugTable(tables.Table):
    class Meta:
        model = Drug

# class DrugFilter(tables.SingleTableMixin,filters.views.FilterView):
#     table_class = DrugTable
#     model = Drug


class DrugFilterSet(filters.FilterSet):
    class Meta:
        model = Drug
        fields = {
            "gtin": ["contains"],
            "dose": ["contains"]
        }