from django.db import models


# Create your models here.
# 기업 정보
class Company(models.Model):
    name = models.CharField(max_length=50)  # 기업명
    sido = models.CharField(max_length=50)  # 기업 위치 (시도)
    sigg = models.CharField(max_length=50)  # 기업 위치(시군구)

    def __str__(self):
        return f'[기업]{self.name} [주소]{self.sido} {self.sigg}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "sido", "sigg"],
                name="unique fields for each company"
            )
        ]


# 직무 정보
class JobPosition(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 직무 이름
    description = models.TextField(blank=True)  # 직무 설명

    def __str__(self):
        return f'[직무]{self.name} [설명]{self.description}'


# 기술스택 정보
class TechStack(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 순위 매기기 위해서 중복값 허용
    type = models.CharField(max_length=50, blank=True)
    companies = models.ManyToManyField('Company', related_name='tech_stacks')  # 기업 정보와 다대다 관계 정의
    job_positions = models.ManyToManyField('JobPosition', related_name='tech_stacks')  # 직무 정보와 다대다 관계 정의

    def __str__(self):
        return f'[기술]{self.name} [분류]{self.type}'






