from django.shortcuts import render
from .models import *
#from .forms import SearchForm
from django.http import JsonResponse


# Create your views here.
def index(request):
    job_positions = JobPosition.objects.all()
    location_sido = Location.objects.filter(parent=None)
    location_sigg = Location.objects.none()

    context = {
        'job_positions': job_positions,
        'location_sido': location_sido,
        'location_sigg': location_sido,
    }

    return render(request, 'main/index.html', context)

def get_sigg_list(request):
    selected_sido = request.GET.get('sido')
    sigg_list = Location.objects.filter(parent__name=selected_sido).values('id', 'name')
    return JsonResponse(list(sigg_list), safe=False)


def result_view(request) :
    if request.method == 'POST' :
        selected_job_position = request.POST.get('job_position')
        selected_sido = request.POST.get('location_sido')
        selected_sigg = request.POST.get('location_sigg')

        context = {
            'selected_job_position' : selected_job_position,
            'selected_sido' : selected_sido,
            'selected_sigg' : selected_sigg,
        }

        return render(request, 'main/result.html', context)


def temp_index(request):
    return render(request, 'main/temp_index.html', {})

def temp_result(request) :
    return render(request, 'main/temp_result.html', {})