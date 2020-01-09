from django.shortcuts import render, redirect
from django.http import HttpResponse
import time
import RPi.GPIO as GPIO
import os
import sys
import Adafruit_DHT
import pymysql
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
    # th_list = TH_data.objects.all()
    # th_list.delete()
    # run_state 2 -> 1
    TH = th_model.instance()
    TH.setRunState(1)
    pi_state = TH.getPiState()
    run_state = TH.getRunState()
    print(pi_state)
    print(run_state)
    os.system('sudo python3 /home/pi/Project/TH_Project/appTH/th_run.py')
    return redirect('home')

def csv(request): 
    return render(request,'home.html')

def end(request):
    # run_state 1 -> 2
    TH = th_model.instance()
    TH.setRunState(2)
    return redirect('home')










