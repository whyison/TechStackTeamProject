import json
from main.models import *

#크롤링한 데이터 가져오기
file_names = ['companies_data.json', 'job_positions_data.json', 'tech_stacks_data.json']
data = list()

for file_name in file_names:
    file_path = 'data/' + file_name
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data.append(json.load(json_file))

# 데이터베이스에 적재하는 함수
def store_data(companies_data, job_positions_data, tech_stacks_data):
    for company, job_position, tech_stack in zip(companies_data, job_positions_data, tech_stacks_data):
        t = TechStack.objects.create(name=tech_stack['name'], type=tech_stack['type']) #중복을 허용해서 생성
        j, _ = JobPosition.objects.get_or_create(name=job_position['name'])
        c, _ = Company.objects.get_or_create(name=company['name'], sido=company['sido'], sigg=company['sigg'])

        j.tech_stacks.add(t)
        c.job_positions.add(j)

store_data(data[0], data[1], data[2])