import sys
import datetime

class th_model:
    
    _instance = None
    pi_num = None
    pi_ip = None
    pi_state = None
    run_state = None
    pi_date = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance
    
    def __init__(self):
        global pi_num, pi_ip, pi_state, run_state, pi_date
        self.pi_num = 13
        self.pi_ip = "192.168.243.13"
        self.pi_state = 1
        self.run_state = 2
        self.pi_date = datetime.datetime.now()
        
    # get
    def getPiNum(self):
        return self.pi_num

    def getPiIp(self):
        return self.pi_ip
    
    def getPiState(self):
        return self.pi_state
    
    def getRunState(self):
        return self.run_state
    
    def getPiDate(self):
        return self.pi_date
    
    # set
    def setRunState(self, value):
        self.run_state = value
        
    def setPiDate(self, value):
        self.pi_date = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        
