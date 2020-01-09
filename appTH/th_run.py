import RPi.GPIO as GPIO
import sys
import os
import time
import Adafruit_DHT
import pymysql
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from TH_Project.singletonTH.th_main import th_model

def checkRunState(value):
    if value == 2:
        return True
    elif value == 1:
        return False
    
TH = th_model.instance()

pi_state = TH.getPiState()
run_state = TH.getRunState()
print(pi_state)
print(run_state)

pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

while TH.getPiState():
    if checkRunState(TH.getRunState()) == False:
        continue
    elif checkRunState(TH.getRunState()) == True:
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
            while checkRunState(TH.getRunState()) == True:
               humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
               if humidity is not None and temperature is not None and humidity < 120 :
                   print('Temp=%0.1f*C Humidity=%0.1f'%(temperature, humidity))
                   time.sleep(9)
                   end=time.time()
                   cur.execute(sql,
                               ((end-start),
                               temperature,humidity))
                   conn.commit()
        except KeyboardInterrupt:
           exit()
        finally :
           conn.close()

print(end)
