from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import *
from .table import *
import django_filters.filterset as filterset

def index(request):

    drugs = Drug.objects.all()

    sortBy = request.GET.get("sort")
    if sortBy:
        drugs = drugs.order_by(sortBy)

    filter = DrugFilterSet(request.GET, queryset=drugs)

    drugTable = DrugTable(filter.qs).paginate(page=request.GET.get("page",1),per_page=25)
    template = loader.get_template('medsApp/mainpage.html')

    def pack(*names, locals=None):
        if locals is None:
            locals = {}
        return {key: locals.get(key, globals().get(key)) for key in names}

    context = pack("drugTable","filter",locals=locals())
    return HttpResponse(template.render(context, request))
