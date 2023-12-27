from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize, deserialize
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def sample_method(request):
    print(request)
    print('---------BODY-----------')
    print(request.body)
    print('------DESerialized------')
    print([item for item in deserialize("json", request.body)])
    print('---------POST-----------')
    print(request.POST)
    print('---------GET------------')
    print(request.GET)
    return JsonResponse({'heh':'heh'})