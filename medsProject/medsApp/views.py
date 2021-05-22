from django.shortcuts import render
from django.db.models import Min

from django.http import HttpResponse
from django.template import loader
from .models import *
from .table import *
import django_filters.filterset as filterset

def index(request):

    filter = DrugFilterSet(request.GET, queryset=Drug.objects.all())

    drugs = filter.qs

    earliest = drugs.order_by('date')[0].date
    diff_pk_none = drugs.filter(diff_pk=None)
    drugs = drugs.filter(date=earliest).exclude(diff_pk=None)

    drugs = drugs | diff_pk_none

    sortBy = request.GET.get("sort")
    if sortBy:
        if sortBy[:5] == 'diff_':
            sortBy = sortBy[5:]
        drugs = drugs.order_by(sortBy)

    drugTable = DrugTable(drugs).paginate(page=request.GET.get("page",1),per_page=25)
    template = loader.get_template('medsApp/mainpage.html')

    def pack(*names, locals=None):
        if locals is None:
            locals = {}
        return {key: locals.get(key, globals().get(key)) for key in names}

    context = pack("drugTable","filter",locals=locals())
    return HttpResponse(template.render(context, request))
