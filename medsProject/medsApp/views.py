from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import *
from .table import *

def index(request):

    drugs = Drug.objects.all()

    sortBy = request.GET.get("sort")
    if sortBy:
        drugs = drugs.order_by(sortBy)

    filterSlug = request.GET.get("filter")
    filters = None
    if filterSlug:
        filters = dict([singleFilter.split(":",1) for singleFilter in filterSlug.split(",")])
        # also allow matches which contain the searched keyword
        lazyFilters = {(key+"__contains"):value for (key,value) in filters.items()}
        drugs = drugs.filter(**lazyFilters)

    drugTable = DrugTable(drugs).paginate(page=request.GET.get("page",1),per_page=25)

    template = loader.get_template('medsApp/mainpage.html')

    def pack(*names, locals=None):
        if locals is None:
            locals = {}
        return {key: locals.get(key, globals().get(key)) for key in names}

    context = pack("drugTable",locals=locals())
    return HttpResponse(template.render(context, request))

# Create your views here.
