import json
import os
from django.core.management.base import BaseCommand, CommandError
from main.models import *
from django.db import transaction

from .location_date import SIDO_DATA, SIGG_LIST

current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)

already_run = False
NUMBER_OF_FILES = 3

# 데이터 적재
class Command(BaseCommand):
    help = "데이터 삭제와 업로드를 관리합니다. --delete로 모든 기존 데이터를 삭제하고, \
        --load로 새 데이터를 업로드합니다. --delete 사용 전 중요 데이터는 백업하세요."

    # -> 매번 데이터를 적재하고 잘못된 데이터 또는 내가 원하지 않은 데이터가 들어갔을 때 어떻게 해야할까?
    # 초기화하고 다시 넣어야하는데 어떻게 해야할까 생각하다가 이렇게 구현함 (다른 방법도 찾아보자)
    def add_arguments(self, parser): 
        parser.add_argument('-d', '--delete', action='store_true', dest='delete', help='Delete existing data')
        parser.add_argument('-l', '--load', action='store_true', dest='load', help='Load data into the database')


    def handle(self, *args, **options):
        if options['delete']:
            # 데이터 삭제 로직
            self.stdout.write('Deleting data...')
            # 데이터 삭제 코드 구현
            self.all_delete()
            self.stdout.write(self.style.SUCCESS('데이터 전체 삭제가 성공적으로 완료되었습니다.'))

        if options['load']:
            # 데이터 로딩 로직
            self.stdout.write('Loading data...')
            # 데이터 로딩 코드 구현
            data = self.load_json_data(os.path.join(current_directory, 'crawling_data'))
            # 적재 해야하는 파일 개수 지정(crwaling_data안에 있는 데이터)
            if len(data) < NUMBER_OF_FILES: 
                raise ValueError("Insufficient data provided. \
                                Expected data for companies, job positions, and tech stacks.")
            
            self.main_load_function(data)
            self.stdout.write(self.style.SUCCESS('데이터 업로드가 성공적으로 완료되었습니다.'))
        

    # 파일에서 JSON 데이터를 읽어오는 함수
    def load_json_data(self, folder_path):
        file_list = list()
        for file_name in os.listdir(folder_path):
            # 파일이 .json 확장자로 끝나는지 확인
            if file_name.endswith('.json'):
                file_path = os.path.join(folder_path, file_name)

                with open(file_path, 'r', encoding='utf-8') as json_file:
                    file_list.append(json.load(json_file))
        return file_list


    # 회사, 직무, 기술 스택 데이터 적재
    @transaction.atomic
    def load_data(self, data):
        for company, job_position, tech_stack in zip(*data):
            jp, _ = JobPosition.objects.get_or_create(name=job_position['name'], 
                                                                        defaults={
                                                                            'description': job_position['description']
                                                                        })
            comp, _ = Company.objects.get_or_create(name=company['name'], 
                                                                sido=company['sido'],
                                                                sigg=company['sigg'])

            ts= TechStack.objects.create(name=tech_stack['name'], type=tech_stack['type'])
            ts.companies.add(comp)
            ts.job_positions.add(jp)


    # 위치 데이터 적재 -> 위치 데이터는 크롤링 후 직접 가져옴 (코드 자동화 개선 필요)
    def load_location(self):
        sigg_data = {}

        for i in range(len(SIDO_DATA)) : 
            sigg_data[SIDO_DATA[i]] = SIGG_LIST[i]

        for i in sigg_data: 
            Location.objects.create(name = i)

        for i in range(len(SIGG_LIST)):
                for j in SIGG_LIST[i]:
                    Location.objects.create(name=j, parent=Location.objects.all()[i])


    # DB에 있는 데이터 전체 삭제
    @transaction.atomic
    def all_delete(self):
        Company.objects.all().delete()
        JobPosition.objects.all().delete()
        TechStack.objects.all().delete()
        Location.objects.all().delete()


    #모든 데이터를 적재하는 함수 (순서 주의 -> 어떻게 해결? -> 정렬 수행?)
    def main_load_function(self, data):
        global already_run
        if not already_run:

            self.load_data(data)
            self.load_location()

        already_run = True



'''
<주의사항 및 개선점 기록>

- 하드 코딩 : 현재 load_location 메소드에서 위치 데이터가 하드 코딩되어 있다. 
이는 유지 관리 측면에서 비효율적일 수 있으며, 데이터 변경시 코드 수정이 필요하다.

- 에러 핸들링 : 스크립트는 기본적인 에러 핸들링을 포함하고 있지만, 더 많은 예외 처리와 로킹을 추가하여 견고성을 높여야 한다.

- 데이터 검증 : 파일에서 읽은 데이터의 유효성을 검증하는 로직이 포함되어 있지 않다. 
-> 데이터의 정확성과 안정성을 보장하기 위해서
유효하지 않은 데이터가 데이터베이스에 적재되는 것을 방지하기 위한 검증 절차가 추가로 필요하다.



'''