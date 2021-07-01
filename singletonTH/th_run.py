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
                      passwd="8302",
                      db="th_db")

pin = 4     
start = time.time()
count = 1
max_hum = 0
try :
    with conn.cursor() as cur :
        sql="INSERT INTO appTH_th_data (run_id, run_time, run_time_str, run_time_date, temperature, humidity) VALUES(%s,%s,%s,%s,%s,%s)"
        start_sql = "SELECT start_time FROM appTH_th_state"
        max_hum_sql = "UPDATE appTH_th_state SET run_id=%s, run_time_str=%s, max_hum_time=%s, max_hum=%s, max_hum_temp=%s"
        cur.execute(start_sql)
        start_date_res = cur.fetchall()
        while True:
           humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
           if humidity is not None and temperature is not None and humidity < 120 :
               print('Temp=%0.1f*C Humidity=%0.1f'%(temperature, humidity))
               end=time.time()
               runtime = end-start
               runtimedate = start_date_res[0][0] + datetime.timedelta(seconds=runtime)
               cur.execute(sql,
                           (count,runtime,sec2time(end-start, 0),runtimedate,round(temperature,3),round(humidity,3)))
               conn.commit()
               # max database update
               if max_hum < round(humidity,3):
                   max_hum = round(humidity,3)
                   cur.execute(max_hum_sql, (count,sec2time(end-start, 0),runtimedate,round(humidity,3),round(temperature,3)))
                   conn.commit()
               count = count + 1
               time.sleep(29)
               if runtime > 86400:
                   os.system('sudo reboot')
                
except KeyboardInterrupt:
   exit()
finally :
   conn.close()
