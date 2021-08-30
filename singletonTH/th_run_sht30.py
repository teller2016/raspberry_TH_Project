import RPi.GPIO as GPIO
import sys
import os
import time
#import Adafruit_DHT
import pymysql
import datetime
import smbus

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

#sensor = Adafruit_DHT.DHT22

# Get I2C bus
bus = smbus.SMBus(1)
bus.write_i2c_block_data(0x44, 0x2C, [0x06])
time.sleep(0.5)
#.connect로 MySQL에 연결
# 호스트명, 포트, 로그인, 암호, 접속할 DB
conn= pymysql.connect(host="localhost",
                      user="pi",
                      passwd="8302",
                      db="th_db")

#4번 출력핀
pin = 4     
start = time.time()
count = 1
#최대 습도
max_hum = 0
try :
    with conn.cursor() as cur :
        sql="INSERT INTO appTH_th_data (run_id, run_time, run_time_str, run_time_date, temperature, humidity) VALUES(%s,%s,%s,%s,%s,%s)"
        start_sql = "SELECT start_time FROM appTH_th_state"
        max_hum_sql = "UPDATE appTH_th_state SET run_id=%s, run_time_str=%s, max_hum_time=%s, max_hum=%s, max_hum_temp=%s"
        cur.execute(start_sql)
        start_date_res = cur.fetchall()
        
        sleepTime = int(sys.argv[1])
        #print(sleepTime)
        
        #th_state에 데이터가 없을 경우 INSERT한다
        if start_date_res == ():
            print('th_state Data is Empty! - Creating Default th_state Data')
            now = datetime.date.today()
            new_state_sql = "INSERT INTO appTH_th_state (run_id, run_time_str, last_run_id, start_time, end_time, max_hum_time, max_hum, max_hum_temp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(new_state_sql,
                        (0, "00:00:00", 0,
                         now, now, now,
                         0, 0))
            conn.commit()
            cur.execute(start_sql)
            start_date_res = cur.fetchall()
            
                         
        #cur.execute("DELETE FROM appTH_th_data")
        #conn.commit()
        #print(datetime.date.today())
        #now = datetime.date.today()

        while True:
            data = bus.read_i2c_block_data(0x44, 0x00, 6)
            temperature = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
            humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
           #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            if humidity is not None and temperature is not None and humidity < 120 :
                print('Temp=%0.1f*C Humidity=%0.1f'%(temperature, humidity))
                end=time.time() #end = 현재 시간
                runtime = end-start #진행한 시간 = 현재시간 - 시작시간
               
               # timeDelta() = 두 시간의 차이를 보여준다? (진행한 시간)
               # th_state에 속한 가장 최신 시간에, 진행한 시간을 더해준다.
                runtimedate = start_date_res[0][0] + datetime.timedelta(seconds=runtime)
               
            
               #cur.execute(sql,
                #           (count,runtime,sec2time(end-start, 0),runtimedate,round(temperature,3),round(humidity,3)))
               #conn.commit()
               # max database update
                if max_hum <= round(humidity,3):
                    print('Max Humid value appeared!!')
                    max_hum = round(humidity,3)
                    cur.execute(max_hum_sql, (count,sec2time(end-start, 0),runtimedate,round(humidity,3),round(temperature,3)))
                    conn.commit()
                count = count + 1
                time.sleep(sleepTime)
                if runtime > 86400: # reboot PI after 24 hours
                   os.system('sudo reboot')
                
except KeyboardInterrupt:
   exit()
finally :
   conn.close()
