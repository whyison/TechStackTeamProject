from django.db import models

# Create your models here.
# 기업 정보
class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)            # 기업명
    address = models.CharField(max_length=100, default='없음')     # 기업 위치(주소)
    job_positions = models.ManyToManyField('JobPosition', related_name='companies') 
    # 직무 정보와 다대다 관계 정의
    
    def __str__(self):
        return f'기업: {self.name}'

# 직무 정보
class JobPosition(models.Model):
    name = models.CharField(max_length=50, unique=True)           # 직무 이름
    description = models.TextField(default='없음')                # 직무 설명
    tech_stacks = models.ManyToManyField('TechStack', related_name='job_positions') 
    # 기술스택 정보와 다대다 관계 정의

    def __str__(self):
        return f'직무:{self.name}, 설명:{self.description}'
        

# 기술스택 정보
class TechStack(models.Model):
    CATEGORY_CHOICES = ( # 카테고리 추가 가능 -> software | tool..등
        ('language', 'Language'),
        ('framework', 'Framework'),
        ('tool', 'Tool')
    )
    name = models.CharField(max_length=50, unique=True) 
    type = models.CharField(max_length=20, choices=CATEGORY_CHOICES) # 보류
    icon_url = models.URLField(blank=True)  # 선택사항

    def __str__(self):
        return f'기술: {self.name}, 유형:{self.type}'






