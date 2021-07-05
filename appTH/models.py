from django.db import models
from datetime import datetime
# Create your models here.

class TH_data(models.Model):
    run_id = models.IntegerField() #하나의 데이터 셋의 각 데이터의 고유 id값
    run_time = models.IntegerField() #(정수값) 기록이 진행된 초
    run_time_str = models.CharField(max_length=10) #(문자열) 기록이 진행된 초 (ex. 00:00:XX)
    run_time_date = models.DateTimeField(default=datetime.now, blank=True) # ??? 값이 측정된 시간 ( 날짜 + 시간 )
    temperature = models.FloatField() # 온도값
    humidity = models.FloatField() # 습도값

class TH_state(models.Model):
    run_id = models.IntegerField(default = 1) # 저장된 run_id
    run_time_str = models.CharField(max_length=10) #(문자열) 기록이 진행된 초 (ex. 00:00:XX)
    last_run_id = models.IntegerField() # ??? 변경되기 이전의 run_id값
    start_time = models.DateTimeField(default=datetime.now, blank=True) # 시작 시간 (날짜 + 시간)
    end_time = models.DateTimeField(default=datetime.now, blank=True) # 종료 시간 (날짜 + 시간)
    max_hum_time = models.DateTimeField(default=datetime.now, blank=True) # 최대 습도 측정된 시간 (날짜 + 시간)
    max_hum = models.FloatField() #  최대 습도값
    max_hum_temp = models.FloatField() # 최대 온도값
    