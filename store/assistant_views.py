import json
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .assistant import respond

@require_POST
def assistant_chat(request):
    if len(request.body) > 4096:
        return JsonResponse({"error": "Message too long"}, status=400)
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    message = data.get("message") if isinstance(data, dict) else None
    if not isinstance(message, str) or not message.strip() or len(message) > 500:
        return JsonResponse({"error": "Please enter a message (up to 500 characters)."}, status=400)
    # Basic throttle per session and minute; production can use Redis for shared rate limits.
    if not request.session.session_key:
        request.session.create()
    import time
    bucket = int(time.time() // 60)
    key = "chat:%s:%s" % (request.session.session_key, bucket)
    if cache.get(key, 0) >= 12:
        return JsonResponse({"error": "Too many messages. Try again in a minute."}, status=429)
    try:
        cache.add(key, 0, timeout=75)
        cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=75)
    answer, mode = respond(message.strip())
    return JsonResponse({"reply": answer, "mode": mode})
