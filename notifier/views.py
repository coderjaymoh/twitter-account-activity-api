from django.shortcuts import render
from .listen import Notify
from django.conf import settings

def index(request):
    return render(request, 'index.html', {})

def listener(request):
    notify = Notify()
    # notify.register_url()
    # msg = request.GET.get('crc_token')
    # print(msg)
    # print(request.GET)
    notify.token(settings.CONSUMER_API_SECRET_KEY)

    return render(request, 'api/listener.html', {})