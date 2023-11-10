import json
import os
# from django.db import transaction
from main.models import *


already_run = False

# 파일에서 JSON 데이터를 읽어오는 함수
def load_json_data(file_name):
    file_path = os.path.join('data', file_name)
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def load_data(companies_data, tech_stacks_data, job_positions_data):
        for company, job_position, tech_stack in zip(companies_data, job_positions_data, tech_stacks_data):
            jp, job_position_created = JobPosition.objects.get_or_create(name=job_position['name'], 
                                                                        defaults={
                                                                            'description': job_position['description']
                                                                        })
            comp, company_created = Company.objects.get_or_create(
                                                            name=company['name'],
                                                            defaults={
                                                                'sido' : company['sido'],
                                                                'sigg' : company['sigg']
                                                            })

            ts= TechStack.objects.create(name=tech_stack['name'], type=tech_stack['type'])
            ts.companies.add(comp)
            ts.job_positions.add(jp)


# 메인 함수: 모든 데이터를 적재하는 함수
def main_load_function():
    global already_run
    if not already_run:
    # JSON 데이터를 로드
        tech_stacks_data = load_json_data('tech_stacks_result.json')
        job_positions_data = load_json_data('job_positions_result.json')
        companies_data = load_json_data('companies_data_result.json')
        # 데이터를 적재
        load_data(companies_data, tech_stacks_data, job_positions_data)
    already_run = True