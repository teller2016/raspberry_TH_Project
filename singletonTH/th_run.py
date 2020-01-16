import RPi.GPIO as GPIO
import sys
import os
import time
import Adafruit_DHT
import pymysql
import datetime

pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

sensor = Adafruit_DHT.DHT22
conn= pymysql.connect(host="localhost",
                      user="pi",
                      passwd="",
                      db="th_db")

pin = 4     
start = time.time()
try :
   with conn.cursor() as cur :
    sql="INSERT INTO appTH_th_data (run_time, temperature, humidity) VALUES(%s,%s,%s)"
    while True:
       humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
       if humidity is not None and temperature is not None and humidity < 120 :
           print('Temp=%0.1f*C Humidity=%0.1f'%(temperature, humidity))
           time.sleep(9)
           end=time.time()
           cur.execute(sql,
                       (end-start,round(temperature,3),round(humidity,3)))
           conn.commit()
           
except KeyboardInterrupt:
   exit()
finally :
   conn.close()
