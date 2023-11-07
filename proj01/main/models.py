from django.db import models

# Create your models here.
# 기업 정보
class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)            # 기업명
    sido = models.CharField(max_length=50, default='시도') # 기업 위치 (시도)
    sigg = models.CharField(max_length=50, default='시군구')     # 기업 위치(시군구)
    job_positions = models.ManyToManyField('JobPosition', related_name='companies') 
    # 직무 정보와 다대다 관계 정의
    
    def __str__(self):
        return f'기업: {self.name}'

# 직무 정보
class JobPosition(models.Model):
    name = models.CharField(max_length=50, unique=True)           # 직무 이름
    description = models.TextField(blank=True)                # 직무 설명
    tech_stacks = models.ManyToManyField('TechStack', related_name='job_positions') 
    # 기술스택 정보와 다대다 관계 정의

    def __str__(self):
        return f'직무:{self.name}, 설명:{self.description}'
        

# 기술스택 정보
class TechStack(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, blank=True) # 보류
    icon_url = models.URLField(blank=True)  # 선택사항

    def __str__(self):
        return f'기술: {self.name}, 유형:{self.type}'






