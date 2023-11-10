from django.shortcuts import render, get_object_or_404
from django.db.models import Count
import json
from .models import *
import pandas as pd
import plotly.express as px

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def result_view(request) :
    if request.method == 'POST' :
        return render(request, 'main/result.html', {})




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

# def temp_result(request) :

#     #선택된 값 result 페이지에 넘겨서 확인하기
#     job_position = request.POST['job_position']
#     sido = request.POST['sido']
#     sigg = request.POST['sigg']

#     return render(request, 'main/temp_result.html', {'job_position': job_position, 'sido': sido, 'sigg':sigg})


# 차트 그리기
def temp_result(request):
    #선택된 값 result 페이지에 넘겨서 확인하기
    job_position = get_object_or_404(JobPosition, name=request.POST['job_position'])
    tech_stacks = TechStack.objects.filter(job_positions=job_position)

    sido = request.POST['sido']
    sigg = request.POST['sigg']

    tech_type_counts=tech_stacks.values('type').annotate(count=Count('name')).order_by('-count')[:5]    

    charts_html = []  # 차트 HTML을 저장할 리스트

    for tech_stack in tech_type_counts.values('type'):

        cls = tech_stack['type']
        tech_stacks_by_cls = tech_stacks.filter(type=cls)
        #-----
        data = [{'스택': ts.name, '개수': tech_stacks.filter(name=ts.name).count()} for ts in tech_stacks_by_cls]

        unique_data = {}
        for item in data:
            stack_name = item['스택']
            count = item['개수']
            if stack_name not in unique_data:
                unique_data[stack_name] = count

        unique_data_list = [{'스택': key, '개수': value} for key, value in unique_data.items()]

        # '개수' 필드에 따라 내림차순으로 정렬
        sorted_data = sorted(unique_data_list, key=lambda x: x['개수'], reverse=True)

        # 상위 5개 요소 선택
        top_5_data = sorted_data[:5]

        # Plotly 차트 생성
        fig = px.pie(data_frame=top_5_data, values='개수', names='스택', title=f"{job_position.name} 직무의 {cls} 분류 TOP5")
        fig.update_traces(hole=.3)
        fig.update_traces(textposition='inside', textinfo='label+percent+value', textfont_size=17, textfont_color="white")

        # 차트를 HTML 문자열로 변환하고 리스트에 추가
        charts_html.append(fig.to_html(full_html=False))

    context = {
        'charts_html': charts_html, 
        'job_position': job_position, 
        'sido': sido,
        'sigg':sigg
        }


    return render(request, 'main/temp_result.html', context)