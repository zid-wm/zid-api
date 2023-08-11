import json

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from v1.administration.models import (
    ActionLog,
    MAVP
)


@require_http_methods(["POST"])
def new_action_log(request):
    body = json.loads(request.body)
    try:
        action = body['action']
    except KeyError:
        return HttpResponse(status=400)

    if len(action) > 255:
        return HttpResponse(status=400)

    ActionLog(action=action).save()
    return HttpResponse(status=200)


@require_http_methods(["GET"])
def get_action_logs(request):
    page_num = int(request.GET.get('page', 0))
    items = int(request.GET.get('items', 50))

    if items < 1 or page_num < 0:
        return HttpResponse(status=400)

    log_results = ActionLog.objects.all().order_by('-timestamp')
    paginator = Paginator(log_results, per_page=items)
    page = paginator.get_page(page_num)

    return JsonResponse(
        {
            'page': page_num,
            'has_next_page': page.has_next(),
            'has_prev_page': page.has_previous(),
            'actions': list(page.object_list.values())
        },
        status=200,
        safe=False
    )


@require_http_methods(["GET"])
def get_mavp(request):
    mavp_results = MAVP.objects.all()
    return JsonResponse(
        {
            'mavp': list(mavp_results.values())
        },
        status=200
    )


@require_http_methods(["POST"])
def new_mavp(request):
    body = json.loads(request.body)
    try:
        fac_short = body['facility_short']
        fac_long = body['facility_long']
    except KeyError:
        return HttpResponse(status=400)

    if len(fac_short) > 3 or len(fac_long) > 255:
        return HttpResponse(status=400)

    if MAVP.objects.filter(facility_short=fac_short).exists():
        return HttpResponse(status=409)

    MAVP(facility_short=fac_short, facility_long=fac_long).save()
    return HttpResponse(status=200)


@require_http_methods(["DELETE"])
def delete_mavp(request):
    body = json.loads(request.body)
    try:
        fac_short = body['facility_short']
    except KeyError:
        return HttpResponse(status=400)

    if not MAVP.objects.filter(facility_short=fac_short).exists():
        return HttpResponse(status=404)

    MAVP.objects.filter(facility_short=fac_short).delete()
    return HttpResponse(status=200)
