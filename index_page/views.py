# from re import template
from django.shortcuts import render

# Create your views here.
def index_view(request):

    template_name = 'index.html'

    return render(request, template_name)