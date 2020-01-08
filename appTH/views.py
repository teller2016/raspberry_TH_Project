from django.shortcuts import render
from django.http import HttpResponse
import time
import RPi.GPIO as GPIO
import os
import sys
import Adafruit_DHT
import pymysql

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from TH_Project.singletonTH import th_main

def home(request):
    TH = th_main.th_model.instance()
    pi_num = TH.getPiNum()
    pi_ip = TH.getPiIp()
    pi_state = TH.getPiState()
    run_state = TH.getRunState()
    # get data
    return render(request,'home.html',{'pi_num':pi_num, 'pi_ip':pi_ip, 'pi_state': pi_state, 'run_state':run_state})

def DisplayTH(request): #display database
    return render(request,'home.html')

def InsertTH(request): # data insert
    return render(request,'home.html')

def clearTH(request): # database clear
    return render(request,'home.html')










