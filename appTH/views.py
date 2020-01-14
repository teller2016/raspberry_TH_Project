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
    pi_num = TH.getPiNum()
    pi_ip = TH.getPiIp()
    pi_state = TH.getPiState()
    run_state = TH.getRunState()
            
    # 순으로 지정
    th_list = TH_data.objects.all().order_by('-id')

    return render(request,'home.html',{'pi_num':pi_num, 'pi_ip':pi_ip,
                                       'pi_state': pi_state, 'run_state':run_state, 'th_list':th_list})

def restart(request):
    th_list = TH_data.objects.all()
    th_list.delete()
    # run_state 2 -> 1
    TH = th_model.instance()
    TH.setRunState(1)
    # os.system('sudo  python3 /home/pi/Project/TH_Project/appTH/th_run.py')
    os.system('sudo python3 /home/pi/Project/TH_Project/singletonTH/th_run.py &')
    return redirect('home')

def end(request):
    # run_state 1 -> 2
    os.system('sudo pkill -9 -ef th_run')
    TH = th_model.instance()
    TH.setRunState(2)
    # os.system('sudo halt')
    return redirect('home')

def th_csv(request, word):
    # response content type
    response = HttpResponse(content_type='text/csv')
    #decide the file name
    response['Content-Disposition'] = 'attachment; filename="'+word+'.csv"'

    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))

    #write the headers
    writer.writerow([
            smart_str(u"실행시간"),
            smart_str(u"온도"),
            smart_str(u"습도"),
    ])
    #get data from database or from text file....
    #events = event_services.get_events_by_year(year) #dummy function to fetch data
    th_list = TH_data.objects.all()
    for th_data in th_list:
            writer.writerow([
                    smart_str(th_data.run_time_str),
                    smart_str(th_data.temperature),
                    smart_str(th_data.humidity),
            ])
    return response

def graph(request):
    th_list = TH_data.objects.all()
    return render(request, 'graph.html', {'th_list':th_list})








