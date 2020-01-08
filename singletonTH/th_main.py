import RPi.GPIO as GPIO
import sys
import time
import Adafruit_DHT
import pymysql

class th_model:
    pymysql.version_info = (1, 3, 13, "final", 0)
    pymysql.install_as_MySQLdb()
    
    _instance = None
    pi_num = None
    pi_ip = None
    pi_state = None
    run_state = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance
    
    def __init__(self):
        global pi_num, pi_ip, pi_state, run_state
        pi_num = 13
        pi_ip = "192.168.0.13"
        pi_state = 1
        run_state = 2
        
    # get
    def getPiNum(self):
        return self.pi_num

    def getPiIp(self):
        return self.pi_ip
    
    def getPiState(self):
        return self.pi_state
    
    def getRunState(self):
        return self.run_state
    
    # set
    def setRunState(self, value):
        self.run_state = value

    while pi_state:
        if run_state == 2:
            continue
        elif run_state == 1:
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
                while run_state == 1:
                   humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                   if humidity is not None and temperature is not None and humidity < 120 :
                       print('Temp=%0.1f*C Humidity=%0.1f'%(temperature, humidity))
                       time.sleep(10)
                       end=time.time()
                       cur.execute(sql,
                                   ((end-start),
                                   temperature,humidity))
                       conn.commit()
            except KeyboardInterrupt:
               exit()
            finally :
               conn.close()
