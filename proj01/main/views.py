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
    #데이터베이스에서 직무 가져오기 -> flat=True를 이용해 리스트로 가져옴
    job_position_list = JobPosition.objects.values_list('name', flat=True).distinct()

    #데이터베이스에서 시도 가져오기 -> flat=True를 이용해 리스트로 가져옴
    sido_list = Company.objects.values_list('sido', flat=True).distinct()

    #시도에 해당하는 시군구 가져오기
    sigg_dict = {}
    for sido in sido_list:
        sigg_list = Company.objects.filter(sido=sido).values_list('sigg', flat=True).distinct()
        sigg_dict[sido] = list(sigg_list)

    #자바스크립트에서 딕셔너리 제대로 가져다 쓰기 위해 json 형식으로
    sigg_dict_json = json.dumps(sigg_dict)

    return render(request, 'main/temp_index.html', {'job_position_list' : job_position_list, 'sido_list':sido_list, 'sigg_dict_json':sigg_dict_json})

def temp_result(request) :

    #선택된 값 result 페이지에 넘겨서 확인하기
    job_position = request.POST['job_position']
    sido = request.POST['sido']
    sigg = request.POST['sigg']

    return render(request, 'main/temp_result.html', {'job_position': job_position, 'sido': sido, 'sigg':sigg})