from django.shortcuts import render, redirect
from django.http import HttpResponse
import time
import RPi.GPIO as GPIO
import os
import sys
import Adafruit_DHT
import pymysql
import csv
from django.utils.encoding import smart_str
from .models import * #models.py에 있는 TH_data, TH_state 모델? import
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from TH_Project.singletonTH.th_main import th_model

import random
import datetime
import time
import json
import pandas as pd

import fnmatch

from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse

pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

def getThData(request):
    th_list_mini = TH_data.objects.all().order_by('-id')[:40]
    data = serializers.serialize('json', th_list_mini)
    
    return HttpResponse(data, content_type='text/json-commnet-filtered')
    
def getThState(request):
    th_state = TH_state.objects.all() 
    data = serializers.serialize('json', th_state)

    return HttpResponse(data, content_type='text/json-commnet-filtered')

def getAllThData(request):
    th_list = TH_data.objects.all().order_by('-id')
    data = serializers.serialize('json', th_list)
    
    return HttpResponse(data, content_type='text/json-commnet-filtered')

def home(request):
    TH = th_model.instance() #th_model의 인스턴스 생성? (라즈베리파이 데이터 생성?)
    run_state = TH.getRunState() #th_model의 getRunState()메소드... run_state값 반환
    pi_date = TH.getPiDate() # pi_date값 반환 (현재 시간?)

    th_list = TH_data.objects.all().order_by('-id') # th_data를 id 내림차순으로 정렬 (가장 최근 데이터부터 정렬)
    th_state = TH_state.objects.first() #th_state의 처음에 있는 데이터 가지고 오기

    # create new th_state when there is no data (*prevent error)
    if th_state is None:
        th_state = TH_state()
        th_state.last_run_id = 0
        th_state.start_time = TH.getPiDate()
        th_state.end_time = TH.getPiDate()
        th_state.max_hum_time = TH.getPiDate()
        th_state.max_hum = 0
        th_state.max_hum_temp = 0
        th_state.run_time_str = "-"
        th_state.save()
    
    if run_state == 2:
        th_update = TH_data.objects.last() #가장 마지막에 측정된 데이터 불러옴
        if th_state and th_update:
            th_state.end_time = th_update.run_time_date #th_state의 end_time을 가장 마지막에 측정한 '진행시간'으로 변경
            th_state.save() #값 수정후 저장
    
    num = th_state.run_id #th_state의 run_id값
    th_list_mini = TH_data.objects.all().order_by('-id')[:40]
    
    
    #num_max = TH_data.objects.last() #가장 마지막에 측정된 th_data 데이터
    #if num < 20 or num_max.run_id < 40: #th_state의 run_id값이 20미만 || 가장 최근 측정한 데이터가 40개 이하일때
    #    th_list_mini = TH_data.objects.all().order_by('id')[:40] # 오래된 데이터순으로 정렬하여, 40개 까지만 th_list_mini에 할당
    #elif TH_data.objects.filter(run_id=num+20).exists() == False and num_max.run_id > 40: # 전체 데이터에서? th_state의 run_id + 20에 해당하는 데이터가 없고 || 측정중인 데이터의 개수가 40개가 넘어갈 경우
    #    th_list_mini = TH_data.objects.all().order_by('id')[num_max.run_id-40:num_max.run_id] # 40개 이후의 데이터들을 th_list_mini에 할당
    #else:
    #    th_list_mini = TH_data.objects.all().order_by('id')[num-20:num+20] 
    
    # run_state: 현재 pi의 진행시간
    # th_list: 가장 최근 데이터부터 정렬된 th_data
    # pi_date: 라즈베리파이의 현재시간?
    # th_state: th_state 데이터
    # th_state_mini: th_data의 가장 최신 40개?의 데이터
    return render(request,'home.html',{'run_state':run_state, 'th_list':th_list,
                                       'pi_date':pi_date, 'th_state':th_state, 'th_list_mini':th_list_mini})

def restart(request, word, second): #word: ex> "2021-07-06 17:13:00" // second: repeat time
    TH = th_model.instance() #라즈베리파이 정보 객체 생성
    th_state = TH_state.objects.all() #th_state 데이터 테이블 전체 불러옴
    TH.setPiDate(word) #라즈베리파이 정보 객체 pi_date값 할당
    
    #backup last data
    th_state = TH_state.objects.first()
    conn = pymysql.connect(host='localhost', user='pi', password='8302' ,db='th_db', charset='utf8')
    query = 'SELECT run_time_str, humidity, temperature, run_time_date FROM appTH_th_data' # th_data 전체 데이터 쿼리
    df = pd.read_sql_query(query,conn) # 쿼리 요청에 대한 데이터를 pandas dataframe으로 가져온다
    filename = th_state.start_time.strftime("%Y%m%d_%H%M%S")+".csv" #엑셀 파일이름 지정
    path = "/home/pi/Project/backup/" # 엑셀 파일 저장 경로
    df.to_csv(path+filename, header=True, index=False) # dataframe을 csv 파일로 내보내기
    
    # 1: 온습도계 실행상태
    # 2: 온습도계 종료상태
    TH.setRunState(1) # run_state 2 -> 1
    
    th_list = TH_data.objects.all() # th_data 데이터 테이블 전체 불러옴
    th_list.delete() # th_data 전체 삭제
    th_state.delete() # th_state 삭제
    
    # th_state 새로 생성하고 값 초기화 진행
    new_state = TH_state()
    new_state.last_run_id = 0
    new_state.start_time = TH.getPiDate()
    new_state.end_time = TH.getPiDate()
    new_state.max_hum_time = TH.getPiDate()
    new_state.max_hum = 0
    new_state.max_hum_temp = 0
    new_state.run_time_str = "-"
    new_state.save()
    
    conn.close()
    os.system('sudo python3 /home/pi/Project/TH_Project/singletonTH/th_run.py ' + second + ' &')
    return redirect('home')

def end(request):
    TH = th_model.instance()
    pi_date = TH.getPiDate()
     
    th_update = TH_data.objects.last()
    if th_update:
        th_update.run_time_date = pi_date + datetime.timedelta(seconds=th_update.run_time)
        th_update.save()
    
    os.system('sudo pkill -9 -ef th_run')

    TH.setRunState(2) # run_state 1 -> 2
    return redirect('home')

def th_csv(request, word):
    TH = th_model.instance()
    pi_num = TH.getPiNum()
    # response content type
    response = HttpResponse(content_type='text/csv')
    #decide the file name
    response['Content-Disposition'] = 'attachment; filename="'+word+'.csv"'

    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))

    #write the headers
    writer.writerow([
            smart_str(u"파이번호"),
            smart_str(u"경과시간"),
            smart_str(u"습도"),
            smart_str(u"온도"),
            smart_str(u"실제시간"),
    ])
    #get data from database or from text file....
    #events = event_services.get_events_by_year(year) #dummy function to fetch data
    th_list = TH_data.objects.all()
    for th_data in th_list:
            writer.writerow([
                    smart_str(pi_num),
                    smart_str(th_data.run_time_str),
                    smart_str(th_data.humidity),
                    smart_str(th_data.temperature),
                    smart_str(th_data.run_time_date.strftime("%Y-%m-%d %H:%M:%S")),
            ])
    return response

def graph(request):
    th_list = TH_data.objects.all() #th_data 데이터 전체 할당
    return render(request, 'graph.html', {'th_list':th_list})

def result(request):
    TH = th_model.instance()
    run_state = TH.getRunState()
    
            
    return render(request, 'result.html', {'run_state':run_state})


path = "/home/pi/Project/backup/"

def beforeResult(request):
    
    
    csv_list = os.listdir(path)
    #csv_list = fnmatch.filter(os.listdir(path), "2021*54.csv")
    
    print(csv_list)
    
    year = set()
    month = set()
    day = set()
    hour = set()

    for name in csv_list:#name ex. '20210706_171054.csv'
        year.add(name[:4])
        month.add(name[4:6])
        day.add(name[6:8])
        hour.add(name[9:11])

    #print(list(year))
    #with open(path+'20210708_171054.csv', 'r') as f:
    #    reader = csv.reader(f)
    #    
    #    print(reader)
    #    
    #    for txt in reader:
    #        print(txt)
    
    
    return render(request, 'beforeResult.html', {'csv_list': csv_list,
                                                 'year_list': sorted(list(year), key=int), 'month_list':sorted(list(month), key=int),
                                                 'day_list': sorted(list(day), key=int), 'hour_list':sorted(list(hour), key=int)})

def getByTime(request):
    jsonObject = json.loads(request.body)
    year = jsonObject.get('year')
    month = jsonObject.get('month')
    day = jsonObject.get('day')
    hour = jsonObject.get('hour')
    
    print(year)
    print(month)
    print(day)
    print(hour)
    
    csv_list = fnmatch.filter(os.listdir(path), "*"+year+"*"+month+"*"+day+"*"+hour+"*.csv")
    print(csv_list)
    
    
    return JsonResponse(jsonObject)



