# Django API Handling
from django.http import JsonResponse
from .models import Profile


def get_break_status(request):
    user = request.GET.get('user_id')
    return JsonResponse({'is_on_break': Profile.objects.get(user=user).is_on_break})