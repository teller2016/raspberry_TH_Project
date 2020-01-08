from django.shortcuts import render
from django.http import HttpResponse
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_DHT
import pymysql

def home(request):
    return render(request,'home.html')

def DisplayTH(request): #display database
    return render(request,'home.html')

def InsertTH(request): # data insert
    return render(request,'home.html')

def clearTH(request): # database clear
    return render(request,'home.html')










