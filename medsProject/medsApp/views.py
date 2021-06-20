from django.shortcuts import render
from django.db.models import Min,F

from django.http import HttpResponse
from django.template import loader
from .models import *
from .table import *
import django_filters.filterset as filterset
import dateutil.parser
import charts

def index(request,date=dateutil.parser.parse("2021-03-01 00:00:00")):

    beforeUserFilter = DrugKey.objects.all().order_by("gtin")

    filter = DrugKeyFilterSet(request.GET, queryset=beforeUserFilter)

    drugs = filter.qs

    sortBy = request.GET.get("sort")
    if sortBy:
        if sortBy[:5] == 'diff_':
            sortBy = sortBy[5:]
        drugs = drugs.order_by(sortBy)

    drugKeyTable = DrugKeyTable(drugs).paginate(page=request.GET.get("page",1),per_page=25)
    template = loader.get_template('medsApp/mainpage.html')

    def pack(*names, locals=None):
        if locals is None:
            locals = {}
        return {key: locals.get(key, globals().get(key)) for key in names}

    context = pack("drugKeyTable", "filter", locals=locals())
    for med in DrugKey.objects.all():
        context[med.gtin + med.registered_funding + med.nonregistered_funding] = charts.get_data_source(med)
    return HttpResponse(template.render(context, request))
