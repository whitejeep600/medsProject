import django_tables2 as tables
from .models import *

class DrugTable(tables.Table):
    class Meta:
        model = Drug
