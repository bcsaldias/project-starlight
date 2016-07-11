from django.http import HttpResponse
from django.shortcuts import render


def macho_list(request):
    return HttpResponse("MACHO List")


def macho_detail(request, macho_id):

    # POST

    return HttpResponse("MACHO Detail - ID: %s" % macho_id)
