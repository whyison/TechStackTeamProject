import json
import plotly.express as px

from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from .models import *


# Create your views here.
def index(request):
    job_positions = JobPosition.objects.all()
    location_sido = Location.objects.filter(parent=None)
    location_sigg = Location.objects.none()

    context = {
        'job_positions': job_positions,
        'location_sido': location_sido,
        'location_sigg': location_sigg,
    }

    return render(request, 'main/index.html', context)

def get_sigg_list(request):
    selected_sido = request.GET.get('sido')
    sigg_list = Location.objects.filter(parent__name=selected_sido).values('id', 'name')
    return JsonResponse(list(sigg_list), safe=False)


# 결과 페이지
def result_view(request) :
    
    # 선택한 지역의 신입 개발 직무 텍스트 대입
    if request.method == 'POST' :
        selected_job_position = request.POST.get('job_position')
        selected_sido = request.POST.get('location_sido')
        selected_sigg = request.POST.get('location_sigg')

        if selected_job_position is None:
            messages.error(request, '직무를 선택해주세요.')
            return HttpResponseRedirect(reverse('main:main'))
        
        if selected_sido == None :
            selected_sido = '전국'
        if selected_sigg == None :
            selected_sigg = ''
    

    if selected_sido == '전국':
        job_positing_counts = TechStack.objects.filter(
            job_positions__name=selected_job_position,
        ).count()
    elif selected_sigg == '':
        job_positing_counts = TechStack.objects.filter(
            companies__sido=selected_sido,
            job_positions__name=selected_job_position,
        ).count()
    else:
        job_positing_counts = TechStack.objects.filter(
            companies__sido=selected_sido,
            companies__sigg=selected_sigg,
            job_positions__name=selected_job_position,
        ).count()

    # 선택한 직무에 따른 결과 처리 : 직무별 시각화 그래프
    try:
        job_position = get_object_or_404(JobPosition, name=request.POST['job_position'])
    except Http404:
        messages.error(request, '다시 선택해주세요.')
        return HttpResponseRedirect(reverse('main:main'))
    else:
        tech_stacks = TechStack.objects.filter(job_positions=job_position)

        tech_type_counts = tech_stacks.values('type').annotate(count=Count('name')).order_by('-count')[:5]

        charts_html = []  # 차트 HTML을 저장할 리스트

        for tech_stack in tech_type_counts.values('type'):

            cls = tech_stack['type']
            tech_stacks_by_cls = tech_stacks.filter(type=cls)
            # -----
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
            if len(sorted_data) < 5 :
                fig = px.pie(data_frame=sorted_data, values='개수', names='스택', title=f"{cls}")
            else :
                fig = px.pie(data_frame=top_5_data, values='개수', names='스택', title=f"{cls} TOP5")
            fig.update_traces(hole=.3)
            fig.update_traces(textposition='inside', textinfo='label+percent', textfont_size=14, textfont_color="white")

            fig.update_layout(
                title_x=0.5,  # 제목 가운데 정렬
                showlegend=True,  # 범례 표시 여부
                legend=dict(
                    orientation="h",  # 범례 가로 방향
                    yanchor="bottom",  # 범례 기준점
                    y=-0.3,  # 범례 위치
                    xanchor="center",  # 범례 중앙 정렬
                    x=0.5,  # 범례 중앙 정렬
                ),
            )

            # 차트를 HTML 문자열로 변환하고 리스트에 추가
            charts_html.append(fig.to_html(full_html=False))

        context = {
            'charts_html': charts_html,
            'selected_job_position': selected_job_position,
            'selected_sido': selected_sido,
            'selected_sigg': selected_sigg,
            'selected_job_description': JobPosition.objects.filter(name=selected_job_position).values('description')[0]['description'],
            'job_positing_counts' : job_positing_counts
        }

        return render(request, 'main/result.html', context)