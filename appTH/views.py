from django.shortcuts import render, redirect
from django.http import HttpResponse
import time
import RPi.GPIO as GPIO
import os
import sys
import Adafruit_DHT
import pymysql
import csv
import pandas as pd
from .models import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from TH_Project.singletonTH.th_main import th_model

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
    os.system('sudo python3 /home/pi/Project/TH_Project/singletonTH/th_run.py')
    return redirect('home')

def csv(request, word):
    conn = pymysql.connect(host='localhost', user='pi', password='' ,db='th_db', charset='utf8')
    query = 'SELECT run_time_str, temperature, humidity FROM appTH_th_data'
    df = pd.read_sql_query(query,conn)
    filename = word+".csv"
    df.to_csv(filename, header=True, index=False)
    return redirect('home')

def end(request):
    # run_state 1 -> 2
    TH = th_model.instance()
    TH.setRunState(2)
    # os.system('sudo halt')
    return redirect('home')

def graph(request):
    return render(request,'graph.html')








