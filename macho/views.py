from django.http import HttpResponse
from django.shortcuts import render


def macho_list(request):
    return render(request, 'macho/list.html')


def macho_detail(request, macho_id):

    # POST
    context = {
        'macho': {
            'id': macho_id
        }
    }
    return render(request, 'macho/detail.html', context)
