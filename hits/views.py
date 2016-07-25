import json, math

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def learn(request):
    pass


def hits_list(request):
    with open('hits/pseudouser.json', 'r') as f_data:
        pseudouser = json.load(f_data)
        pseudouser = pseudouser[0]
    pseudouser['is_authenticated'] = True
    pseudouser['progress_hits'] = {
        'max': 2674,
        'num_voted': len(pseudouser['votehits']),
        'percent_complete': len(pseudouser['votehits'])/2674 * 100
    }
    with open('hits/hits_list.json', 'r') as hits_list:
        hits_list = json.load(hits_list)

    page = int(request.GET['page'])
    per_page = 20
    start = (page - 1) * per_page
    end = start+per_page
    max_page = math.ceil(len(hits_list) / 20)

    prev_pg=None
    if page > 1:
        prev_pg = page - 1
    next_pg=None
    if page < max_page:
        next_pg = page + 1

    pages = list(range(1,6,1))
    if page > 4:
        pages = [page+i for i in range(-2,3,1) if 0 < page+i <= max_page]

    context = {
        'hits_list': hits_list[start:end],
        'page': page,
        'next': next_pg,
        'prev': prev_pg,
        'pages': pages,
        'max_page': max_page,
        'user': pseudouser,
        'title': 'hits-list'
    }
    return render(request, 'hits/hits-list.html', context)

@csrf_exempt
def hits_detail(request, hits_id):
    if request.method == "POST":
        json_response = {
            'point': 1,
            'next': 'Blind15A_04_N16_0183_3344'
        }
        return JsonResponse(json_response)
    with open('hits/pseudouser.json', 'r') as f_data:
        pseudouser = json.load(f_data)
        pseudouser = pseudouser[0]
    pseudouser['is_authenticated'] = True
    with open('hits/hits_list.json', 'r') as json_data:
        hits_list = json.load(json_data)
    context = {
        'hits_id': hits_id,
        'saved': True,
        'user': pseudouser,
        'title': 'hits-detail'
    }
    return render(request, 'hits/hits-detail.html', context)


def hits_data(request, hits_id):
    if hits_id == "Blind15A_04_N16_0183_3344":
        json_file = 'rr_lightcurve_list.json'
    else:
        json_file = 'nv_lightcurve_list.json'

    with open('hits/'+json_file, 'r') as json_file:
        lightcurve_data = json.load(json_file)
    with open('hits/hits_list.json', 'r') as json_file:
        hits_list = json.load(json_file)
    hits_profile = None
    for hits in hits_list:
        if hits['hits_id'] == hits_id:
            hits_profile = hits
    json_response = {
        'profile': hits_profile,
        'lightcurve': lightcurve_data
    }
    return JsonResponse(json_response)


# def hits_save(request, hits_id):
#     pass
