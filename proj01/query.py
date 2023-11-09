from django.db.models import Count
from main.models import *


#선택한 직무, 시도, 시군구에 맞는 스택 카운트
def count_tech_stacks_by_name(job_position, sido, sigg):
    tech_stack_counts = TechStack.objects.filter(
        companies__sido=sido,
        companies__sigg=sigg,
        job_positions__name=job_position
    ).values('name').annotate(tech_stack_count=Count('id'))

    #tech_stack_counts는 dictionary 형태의 값을 가지는 리스트
    return tech_stack_counts

#선택한 직무, 시도, 시군구, 스택 유형에 맞는 스택 카운트
def count_tech_stacks_by_type(job_position, sido, sigg, type):
    tech_stack_counts = TechStack.objects.filter(
        companies__sido=sido,
        companies__sigg=sigg,
        job_positions__name=job_position,
        type=type
    ).values('name').annotate(tech_stack_count=Count('id'))

    #tech_stack_counts는 dictionary 형태의 값을 가지는 리스트
    return tech_stack_counts