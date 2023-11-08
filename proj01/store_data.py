import json
import os
from django.db import transaction
from main.models import *


# 크롤링한 데이터
file_names = ['companies_data.json', 'job_positions_data.json', 'tech_stacks_data.json']

# 파일에서 JSON 데이터를 읽어오는 함수
def load_json_data(file_name):
    file_path = os.path.join('data', file_name)
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

# 기술스택&직무 에 데이터를 적재하는 함수
def load_tech_stacks_and_job_postions(tech_stacks_data, job_positions_data):
    for tech_stack, job_position in zip(tech_stacks_data, job_positions_data):
        # 중복을 허용해서 생성
        ts = TechStack.objects.create(name=tech_stack['name'],
                                    type=tech_stack['type'])
        jp, _ = JobPosition.objects.get_or_create(name=job_position['name'])
        jp.tech_stacks.add(ts) # 직무에 기술스택을 연결함

# 기업 데이터를 적재하는 함수
def load_companies(companies_data):
    for company in companies_data:
        comp, _ = Company.objects.get_or_create(name=company['name'],
                                                sido=company['sido'],
                                                sigg=company['sigg'] )
        job_position = JobPosition.objects.get(name=company['job_positions']) # 직무 name이 유니크이기 때문에 get 가능
        comp.job_positions.add(job_position) # 기업에 직무를 연결함


# 메인 함수: 모든 데이터를 적재하는 함수
@transaction.atomic
def main_load_function():
    # JSON 데이터를 로드
    tech_stacks_data = load_json_data('tech_stacks_data.json')
    job_positions_data = load_json_data('job_positions_data.json')
    companies_data = load_json_data('companies_data.json')
    
    # 데이터를 적재
    load_tech_stacks_and_job_postions(tech_stacks_data, job_positions_data)
    load_companies(companies_data)

