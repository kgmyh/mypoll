# account/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import forms
from django.core.exceptions import ValidationError
from datetime import date



# 검증 함수가 많으면 따로 모듈로 뺀다.
# 오늘 날짜 이후 선택시 에러 발생. - clean은 이게 필요한 곳은 다 정의해야 한다. (여기서는 여기만 하면된다.)
def birthday_validator(value):
    # 검증로직만 만들고 검증 실패시 ValidationError 발생시킨다. 통과시는 return None
    print(type(value))
    if value > date.today():
        raise ValidationError("오늘 이전 날짜를 선택하세요.")


## 확장 User 모델 
# - AbstractUser로 구현: 기본 User(username, password)에 필드들을 추가하는 방식
# - AbstractUser 상속. 필드들 정의(username, password빼고 정의)
class User(AbstractUser):
    
    # Field들 정의 - table컬럼
    name = models.CharField(
        verbose_name="이름", # Form관련설정(label) - Form을 ModelForm을 만들 경우 form관련설정을 Model에 한다.
        max_length=50 # varchar(50)
    )
    email = models.EmailField(verbose_name="Email", max_length=100)
    # EmailField: varchar(100) -> 값이 이메일 형식인지(@ 가 있는지)를 검증.
    birthday = models.DateField(
        verbose_name="생일",
        null=True, # Null허용 (default: False - Not Null)
        blank=True # Form - 필수가 아니다.(default: False - required)
        , validators=[birthday_validator] # 검증함수 목록
    )
    profile_img = models.ImageField(
        verbose_name="프로필 사진",
        upload_to="images/%Y/%m/%d", # 저장경로 (media/지정한 경로)
        null=True,
        blank=True
    ) #추가 -> python manage.py makemigrations, migrate
    
    
    def __str__(self):
        return f"Username-{self.username}, Name: {self.name}"

