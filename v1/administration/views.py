import json

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from v1.administration.models import (
    ActionLog,
    MAVP
)


"""
@api {post} /admin/action-log/new Create a new action log entry
@apiName ActionLogNew
@apiGroup Admin
@apiVersion 0.1.0

@apiBody {String{..255}} action
@apiParamExample {json}
    {
        "action": "Action text"
    }

@apiError 400 Bad request
"""
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


"""
@api {get} /admin/action-log/all Get action log entries by page
@apiName ActionLogAll
@apiGroup Admin
@apiVersion 0.1.0

@apiQuery {Number{0..}} page
@apiQuery {Number{1..}} items

@apiSuccess {Number} page Current page displayed.
@apiSuccess {Boolean} has_next_page True if page+1 is a valid page.
@apiSuccess {Boolean} has_prev_page True if page-1 is a valid page.
@apiSuccess {Object[]} actions List of action logs on the current page.
@apiSuccessExample {json}
    {
        "page": 0
        "has_next_page": true
        "has_prev_page": false
        "actions": [
            {
                "id": 50,
                "action": "Action 50",
                "timestamp": "2023-01-01T00:00:00.000Z"
            },
            {
                "id": 49,
                "action": "Action 49",
                "timestamp": "2023-01-01T00:00:00.000Z"
            }
            ...
        ]
    }
"""
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


"""
@api {get} /admin/mavp/all Get all active MAVP agreements
@apiName MAVPAll
@apiGroup Admin
@apiVersion 0.1.0

@apiSuccess {Object[]} mavp List of all active MAVP agreements.
@apiSuccessExample {json}
    {
        "mavp": [
            {
                "facility_short": "ZAB",
                "facility_long": "Academy ARTCC"
            },
            {
                "facility_short": "ZSP",
                "facility_long": "Sample ARTCC"
            }
            ...
        ]
    }
"""
@require_http_methods(["GET"])
def get_mavp(request):
    mavp_results = MAVP.objects.all()
    return JsonResponse(
        {
            'mavp': list(mavp_results.values())
        },
        status=200
    )


"""
@api {post} /admin/mavp/new Create a new MAVP agreement
@apiName MAVPNew
@apiGroup Admin
@apiVersion 0.1.0

@apiBody {String{..3}} facility_short Three-letter abbreviation of the facility
@apiBody {String{..255}} facility_long Long (display) name of the facility
@apiParamExample {json}
    {
        "facility_short": "ZAB",
        "facility_long": "Academy ARTCC"
    }

@apiError 400 Bad request
@apiError 409 MAVP agreement with facility already exists
"""
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


"""
@api {delete} /admin/mavp/delete Delete an existing MAVP agreement
@apiName MAVPDelete
@apiGroup Admin
@apiVersion 0.1.0

@apiBody {String{..3}} facility_short Three-letter abbreviation of the facility
@apiParamExample {json}
    {
        "facility_short": "ZAB"
    }
    
@apiError 400 Bad request
@apiError 404 No MAVP with the specified facility exists
"""
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
