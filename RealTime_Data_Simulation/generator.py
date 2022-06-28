from time import time
import zmq
import math
import time
import random
import pandas as pd

context = zmq.Context() 
socket = context.socket(zmq.PUB) 
socket.bind('tcp://127.0.0.1:5555') 

class InstrumentPrice(object):
    def __init__(self) :
        self.symbol='SYMBOL'
        self.t=time.time()
        self.value=100
        self.sigma=0.4
        self.r=0.01
        
    def sim_val(self):
        t=time.time()
        dt=(t-self.t)/(252*8*60*60)
        dt*=500
        self.t=t
        self.value*=math.exp((self.r-0.5*self.sigma**2)*dt+ self.sigma*math.sqrt(dt)*random.gauss(0,1))
        return self.value
    
ip=InstrumentPrice()
df=pd.DataFrame()
while True:
    msg=f'{ip.symbol}:{ip.sim_val():.2f}'
    print(msg)
    socket.send_string(msg)
    time.sleep(random.random()*2)
    
