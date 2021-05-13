from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import *
from .table import *

def index(request):
    drugTable = DrugTable(Drug.objects.all())

    template = loader.get_template('medsApp/mainpage.html')

    def pack(*names, locals=None):
        if locals is None:
            locals = {}
        return {key: locals.get(key, globals().get(key)) for key in names}

    context = pack("drugTable",locals=locals())
    return HttpResponse(template.render(context, request))

# Create your views here.
