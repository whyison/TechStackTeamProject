from django.test import TestCase
from .models import Company, JobPosition, TechStack
from store_data import *
# Create your tests here.

# Unit Tests
class CompanyModelTests(TestCase):

    # 인스턴스 생성 검증
    def test_instance_creation(self):
        company = Company.objects.create(name="TestName", sido="TestSido", sigg="TestSigg")
        self.assertTrue(isinstance(company, Company))

    # 데이터베이스에 모델 저장되었는지 검증
    def test_store_model_data(self):
        company = Company.objects.create(name="TestName", sido="TestSido", sigg="TestSigg")
        database_company = Company.objects.get(name="TestName", sido="TestSido", sigg="TestSigg")
        self.assertEqual(company, database_company)

    def test_model_str(self):
        company = Company(name="TestName", sido="TestSido", sigg="TestSigg")
        self.assertEqual(str(company), "[기업]TestName [주소]TestSido TestSigg")


class JobPositionModelTests(TestCase):

    def test_instance_creation(self):
        jp = JobPosition.objects.create(name='TestName', description='TestDescription')
        self.assertTrue(isinstance(jp, JobPosition))

    def test_store_model_data(self):
        jp = JobPosition.objects.create(name='TestName', description='TestDescription')
        database_jp = JobPosition.objects.get(name='TestName', description='TestDescription')
        self.assertEqual(jp, database_jp)

    def test_model_str(self):
        jp = JobPosition(name='TestName', description='TestDescription')
        self.assertEqual(str(jp), "[직무]TestName [설명]TestDescription")


class TechStackModelTests(TestCase):
    def test_instance_creation(self):
        ts = TechStack.objects.create(name='TestName', type='TestType')
        self.assertTrue(isinstance(ts, TechStack))

    def test_store_model_data(self):
        ts = TechStack.objects.create(name='TestName', type='TestType')
        database_ts = TechStack.objects.get(name='TestName', type='TestType')
        self.assertEqual(ts, database_ts)

    def test_model_str(self):
        ts = TechStack(name='TestName', type='TestType')
        self.assertEqual(str(ts), "[기술]TestName [분류]TestType")

    def test_many_to_many_relationship(self):
        # 테스트용 기업 및 직무 인스턴스 생성
        company1 = Company.objects.create(name="TestName1", sido="TestSido1", sigg="TestSigg1")
        company2 = Company.objects.create(name="TestName2", sido="TestSido2", sigg="TestSigg2")
        job_position = JobPosition.objects.create(name='TestName')    

        tech_stack = TechStack.objects.create(name='TestName', type='TestType')

        # 다대다 관계 설정
        tech_stack.companies.add(company1, company2)
        tech_stack.job_positions.add(job_position)

        # 다대다 관계가 제대로 설정되었는지 검증
        self.assertEqual(tech_stack.companies.count(), 2)
        self.assertEqual(tech_stack.job_positions.count(), 1)
        self.assertIn(company1, tech_stack.companies.all())
        self.assertIn(company2, tech_stack.companies.all())
        self.assertIn(job_position, tech_stack.job_positions.all())


class StoreDataTests(TestCase):

    def test_different_address_same_name_company(self):
        #테스트용 크롤링 데이터
        companies_data = [
            {'name': 'TestName', 'sido': 'TestSido1', 'sigg': 'TestSigg1'},
            {'name': 'TestName', 'sido': 'TestSido2', 'sigg': 'TestSigg2'},
        ]
        tech_stacks_data = [
            {'name': 'TestName', 'type': 'TestType'},
            {'name': 'TestName', 'type': 'TestType'},
        ]
        job_positions_data = [
            {'name': 'TestName', 'description': 'TestDescription'},
            {'name': 'TestName', 'description': 'TestDescription'},
        ]

        #데이터 적재 메서드
        load_data(companies_data, tech_stacks_data, job_positions_data)

        company_count1 = Company.objects.filter(name='TestName', sido='TestSido1', sigg='TestSigg1').count()
        company_count2 = Company.objects.filter(name='TestName', sido='TestSido2', sigg='TestSigg2').count()
        tech_stack_count = TechStack.objects.filter(name='TestName', type='TestType').count()
        job_position_count = JobPosition.objects.filter(name='TestName', description='TestDescription').count()

        self.assertEqual(company_count1, 1)
        self.assertEqual(company_count2, 1)
        self.assertEqual(tech_stack_count, 2)
        self.assertEqual(job_position_count, 1)

    '''
    #중복 데이터 처리 추후 개발 예정
    def test_duplicated_job_positing(self):
        #테스트용 크롤링 데이터
        companies_data = [
            {'name': 'TestName', 'sido': 'TestSido', 'sigg': 'TestSigg'},
            {'name': 'TestName', 'sido': 'TestSido', 'sigg': 'TestSigg'},
        ]
        tech_stacks_data = [
            {'name': 'TestName', 'type': 'TestType'},
            {'name': 'TestName', 'type': 'TestType'},
        ]
        job_positions_data = [
            {'name': 'TestName', 'description': 'TestDescription'},
            {'name': 'TestName', 'description': 'TestDescription'},
        ]

        #데이터 적재 메서드
        load_data(companies_data, tech_stacks_data, job_positions_data)

        company_count = Company.objects.filter(name='TestName', sido='TestSido', sigg='TestSigg').count()
        tech_stack_count = TechStack.objects.filter(name='TestName', type='TestType').count()
        job_position_count = JobPosition.objects.filter(name='TestName', description='TestDescription').count()

        self.assertEqual(company_count, 1)
        self.assertEqual(tech_stack_count, 1)
        self.assertEqual(job_position_count, 1)
    '''
