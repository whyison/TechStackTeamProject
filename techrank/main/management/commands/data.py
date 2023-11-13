import json
import os
from django.core.management.base import BaseCommand, CommandError
from main.models import *
from django.db import transaction

current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)

already_run = False
NUMBER_OF_FILES = 3

# 데이터 적재
class Command(BaseCommand):
    help = "데이터 삭제와 업로드를 관리합니다. --delete로 모든 기존 데이터를 삭제하고, \
        --load로 새 데이터를 업로드합니다. --delete 사용 전 중요 데이터는 백업하세요."

    # -> 매번 데이터를 적재하고 잘못된 데이터 또는 내가 원하지 않은 데이터가 들어갔으면 
    # -> 잘못된 데이터가 들어간 것은 테스트로 확인이 되지만, 내가 원하지 않은 데이터가 들어간 것은 쉽지 않다..
    # 초기화하고 다시 넣어야하는데 어떻게 해야할까 생각하다가 이렇게 구현함
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
        sido_data = ['전국', '서울', '경기', '인천', '부산', '대구', '광주', '대전', '울산', 
                    '세종', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
        sigg_list = [[],
            ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'], 
            ['가평군', '고양시', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', '동두천시', '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시', '안양시', '양주시', '양평군', '여주시', '연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시'], 
            ['강화군', '계양구', '남동구', '동구', '미추홀구', '부평구', '서구', '연수구', '옹진군', '중구'], 
            ['강서구', '금정구', '기장군', '남구', '동구', '동래구', '부산진구', '북구', '사상구', '사하구', '서구', '수영구', '연제구', '영도구', '중구', '해운대구'], 
            ['군위군', '남구', '달서구', '달성군', '동구', '북구', '서구', '수성구', '중구'],
            ['광산구', '남구', '동구', '북구', '서구'], 
            ['대덕구', '동구', '서구', '유성구', '중구'],
            ['남구', '동구', '북구', '울주군', '중구'], 
            ['가람동', '고운동', '금남면', '나성동', '누리동', '다솜동', '다정동', '대평동', '도담동', '반곡동', '보강면', '보람동', '산울동', '새롬동', '세종동', '소담동', '소정면', '아름동', '어진동', '연기면', '연동면', '연서면', '용호동', '장군면', '전동면', '전의면', '조치원읍', '종촌동', '집현동', '한별동', '한솔동', '합강동', '해밀동'], 
            ['강릉시', '고성군', '동해시', '삼척시', '속초시', '양구군', '양양군', '영월군', '원주시', '정선군', '철원군', '춘천시', '태백시', '평창군', '홍천군', '화천군', '횡성군'], 
            ['괴산군', '단양군', '보은군', '영동군', '옥천군', '음성군', '제천시', '증평군', '진천군', '청주시', '충주시'], 
            ['계룡시', '공주시', '금산군', '논산시', '당진시', '보령시', '부여군', '서산시', '서천군', '아산시', '예산군', '천안시', '청양군', '태안군', '홍성군'], 
            ['고창군', '군산시', '김제시', '남원시', '무주군', '부안군', '순창군', '완주군', '익산시', '임실군', '장수군', '전주시', '정읍시', '진안군'], 
            ['강진군', '고흥군', '곡성군', '광양시', '구례군', '나주시', '담양군', '목포시', '무안군', '보성군', '순천시', '신안군', '여수시', '영광군', '영암군', '완도군', '장성군', '장흥군', '진도군', '함평군', '해남군', '화순군'], 
            ['경산시', '경주시', '고령군', '구미시', '군위군', '김천시', '문경시', '봉화군', '상주시', '성주군', '안동시', '영덕군', '영양군', '영주시', '영천시', '예천군', '울릉군', '울진군', '의성군', '청도군', '청송군', '칠곡군', '포항시'], 
            ['거제시', '거창군', '고성군', '김해시', '남해군', '밀양시', '사천시', '산청군', '양산시', '의령군', '진주시', '창녕군', '창원시', '통영시', '하동군', '함안군', '함양군', '합천군'], 
            ['서귀포시', '제주시'], ]

        sigg_data = {}

        for i in range(len(sido_data)) : 
            sigg_data[sido_data[i]] = sigg_list[i]

        for i in sigg_data: 
            Location.objects.create(name = i)

        for i in range(len(sigg_list)):
                for j in sigg_list[i]:
                    Location.objects.create(name=j, parent=Location.objects.all()[i])


    #모든 데이터를 적재하는 함수 (순서 주의 -> 어떻게 해결? -> 정렬 수행?)
    def main_load_function(self, data):
        global already_run
        if not already_run:

            self.load_data(data)
            self.load_location()

        already_run = True

    # 데이터베이스 reset
    @transaction.atomic
    def all_delete(self):
        Company.objects.all().delete()
        JobPosition.objects.all().delete()
        TechStack.objects.all().delete()
        Location.objects.all().delete()