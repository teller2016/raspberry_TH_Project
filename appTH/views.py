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
import pandas as pd
from .models import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from TH_Project.singletonTH.th_main import th_model

import random
import datetime
import time

pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

def home(request):
    TH = th_model.instance()
    run_state = TH.getRunState()
    pi_date = TH.getPiDate() 
    
    # 순으로 지정
    th_list = TH_data.objects.all().order_by('-id')
    th_state = TH_state.objects.first()
    # datafield update하는 코드 추가하기(상태반영해서 업데이트할 것 - 실행중일때만)

    if run_state == 1:
    # Last id remember
        for th_update in th_list:
            if th_update.run_id > th_state.last_run_id - 2:
                th_update.run_time_date = pi_date + datetime.timedelta(seconds=th_update.run_time)
                th_update.save()
                if th_update.humidity > th_state.max_hum:
                    th_state.run_id = th_update.run_id
                    th_state.run_time_str = th_update.run_time_str
                    th_state.max_hum = th_update.humidity
                    th_state.max_hum_temp = th_update.temperature
                    th_state.max_hum_time = th_update.run_time_date
                th_state.last_run_id = th_update.run_id
                th_state.save()     
    else:
        th_update = TH_data.objects.last()
        if th_state and th_update:
            th_state.end_time = th_update.run_time_date
            th_state.save()

    return render(request,'home.html',{'run_state':run_state, 'th_list':th_list,
                                       'pi_date':pi_date, 'th_state':th_state})

def restart(request, word):
    TH = th_model.instance()
    th_state = TH_state.objects.all()
    TH.setPiDate(word)
    
    #backup last data
    th_state = TH_state.objects.first()
    conn = pymysql.connect(host='localhost', user='pi', password='' ,db='th_db', charset='utf8')
    query = 'SELECT run_time_str, humidity, temperature, run_time_date FROM appTH_th_data'
    df = pd.read_sql_query(query,conn)
    filename = th_state.start_time.strftime("%Y%m%d_%H%M%S")+".csv"
    path = "/home/pi/Project/backup/"
    df.to_csv(path+filename, header=True, index=False)
    
    TH.setRunState(1) # run_state 2 -> 1
    
    th_list = TH_data.objects.all()
    th_list.delete()
    th_state.delete()
    
    new_state = TH_state()
    new_state.last_run_id = 0
    new_state.start_time = TH.getPiDate()
    new_state.end_time = TH.getPiDate()
    new_state.max_hum_time = TH.getPiDate()
    new_state.max_hum = 0
    new_state.max_hum_temp = 0
    new_state.run_time_str = "-"
    new_state.save()
    
    os.system('sudo python3 /home/pi/Project/TH_Project/singletonTH/th_run.py &')
    return redirect('home')

def end(request):
    TH = th_model.instance()
    pi_date = TH.getPiDate()
     
    th_update = TH_data.objects.last()
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
    th_list = TH_data.objects.all()
    return render(request, 'graph.html', {'th_list':th_list})








