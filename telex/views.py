from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import httpx
from celery import shared_task
# Create your views here.



def integration_json(request):
    base_url = request.build_absolute_uri("/")[:-1]
    data = {
        "data": {
            "descriptions": {
                "app_name": "one-health",
                "app_description": "Hospitals Website and operations",
                "app_url": base_url,
                "app_logo": "https://i.imgur.com/lZqvffp.png",
                "background_color": "#fff"
            },
            "integration_type": "interval",
            "settings": [
                {"label": "site-1", "type": "text", "required": True, "default": ""},
                {"label": "site-2", "type": "text", "required": True, "default": ""},
                {"label": "interval", "type": "text", "required": True, "default": "* * * * *"}
            ],
            "tick_url": f"{base_url}/tick"
        }
    }
    return JsonResponse(data)




@shared_task
def monitor_task(channel_id, return_url, sites):
    results = []
    
    for site in sites:
        try:
            response = httpx.get(site, timeout=10)
            if response.status_code >= 400:
                results.append(f"{site} is down (status {response.status_code})")
        except Exception as e:
            results.append(f"{site} check failed: {str(e)}")

    message = "\n".join(results)

    data = {
        "message": message,
        "username": "DistinctDev",
        "event_name": "Appointment Notification",
        "status": "error" if results else "success"
    }

    httpx.post(return_url, json=data)

@csrf_exempt
def tick(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            sites = [s["default"] for s in payload["settings"] if s["label"].startswith("site")]
            monitor_task.delay(payload["channel_id"], payload["return_url"], sites)
            return JsonResponse({"status": "accepted"}, status=202)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
