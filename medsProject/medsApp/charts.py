from .models import *
import json


def get_data_source(drug):
    rows = Drug.objects.filter(gtin=drug.gtin, registered=drug.registered, nonregistered=drug.nonregistered).order_by('date')
    res = []
    for row in rows:
        res.append({'date': row.date, 'payment': row.patient_payment})
    return json.dumps(res, indent=4)
