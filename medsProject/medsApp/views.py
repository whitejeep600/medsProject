from django.shortcuts import render
from django.db.models import Min,F

from django.http import HttpResponse
from django.template import loader
from .models import *
from .table import *
import django_filters.filterset as filterset
import dateutil.parser

def index(request):

    # beforeUserFilter = Drug.objects.all().filter(date=date,last_changed=F("date")).order_by("gtin")
    #
    # filter = DrugFilterSet(request.GET, queryset=beforeUserFilter)
    #
    # drugs = filter.qs
    #
    # sortBy = request.GET.get("sort")
    # if sortBy:
    #     if sortBy[:5] == 'diff_':
    #         sortBy = sortBy[5:]
    #     drugs = drugs.order_by(sortBy)

    beforeUserFilter = DrugKey.objects.all().order_by("gtin")

    filter = DrugFilterSet(request.GET, queryset=beforeUserFilter)

    drugKeys = filter.qs

    sortBy = request.GET.get("sort")

    if sortBy:
        drugKeys = drugKeys.order_by(sortBy)

    drugKeysTable = DrugKeyTable(drugKeys).paginate(page=request.GET.get("page",1),per_page=25)
    template = loader.get_template('medsApp/mainpage.html')

    def pack(*names, locals=None):
        if locals is None:
            locals = {}
        return {key: locals.get(key, globals().get(key)) for key in names}

    context = pack("drugKeysTable", "filter", locals=locals())

    return HttpResponse(template.render(context, request))


def cache(fun):
    x = {}
    def result(*args,**kwargs):
        if (args,kwargs) in x:
            return x[(args,kwargs)]
        x[(args, kwargs)] = fun(*args,**kwargs)
        return x[(args,kwargs)]
    return result