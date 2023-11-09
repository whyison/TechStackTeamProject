from django.test import TestCase
from .models import Company, JobPosition, TechStack
# Create your tests here.

# Unit Tests
class CompanyModelTests(TestCase):
    def test_instance_creation(self):
        company = Company.objects.create(name="TestName", sido="TestSido", sigg="TestSigg")
        self.assertTrue(isinstance(company, Company))

    def test_model_str(self):
        company = Company(name="TestName", sido="TestSido", sigg="TestSigg")
        self.assertEqual(str(company), "[기업]TestName [주소]TestSido TestSigg")


class JobPositionModelTests(TestCase):
    def test_instance_creation(self):
        jp = JobPosition.objects.create(name='TestName', description='TestDescription')
        self.assertTrue(isinstance(jp, JobPosition))

    def test_model_str(self):
        jp = JobPosition(name='TestName', description='TestDescription')
        self.assertEqual(str(jp), "[직무]TestName [설명]TestDescription")


class TechStackModelTests(TestCase):
    def test_instance_creation(self):
        ts = TechStack.objects.create(name='TestName', type='TestType')
        self.assertTrue(isinstance(ts, TechStack))

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