import RPi.GPIO as GPIO
import sys
import os
import time
import Adafruit_DHT
import pymysql
import datetime

def sec2time(sec, n_msec=3):
    ''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
    if hasattr(sec,'__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)

pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

sensor = Adafruit_DHT.DHT22
conn= pymysql.connect(host="localhost",
                      user="pi",
                      passwd="",
                      db="th_db")

pin = 4     
start = time.time()
count = 1
try :
   with conn.cursor() as cur :
    sql="INSERT INTO appTH_th_data (run_id, run_time, run_time_str, temperature, humidity) VALUES(%s,%s,%s,%s,%s)"
    while True:
       humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
       if humidity is not None and temperature is not None and humidity < 120 :
           print('Temp=%0.1f*C Humidity=%0.1f'%(temperature, humidity))
           time.sleep(9)
           end=time.time()
           cur.execute(sql,
                       (count,end-start,sec2time(end-start, 0),round(temperature,3),round(humidity,3)))
           conn.commit()
           count = count + 1
           
except KeyboardInterrupt:
   exit()
finally :
   conn.close()
