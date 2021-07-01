import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from TH_Project.singletonTH.th_main import th_model
th_model.instance()