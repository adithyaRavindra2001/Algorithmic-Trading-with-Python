from datetime import datetime
from locale import currency
from mimetypes import init
import os
from turtle import pos
import zmq 
import pandas as pd
import numpy as np
import time
import random

context = zmq.Context() 
socket = context.socket(zmq.SUB) 
socket.connect('tcp://127.0.0.1:5555') 
socket.setsockopt_string(zmq.SUBSCRIBE, 'SYMBOL') 



def go_long(amount,currentPrice):
    units=amount/currentPrice
    return units
    
def sell(units_traded,currentPrice):
    amount=0
    amount+=units_traded*currentPrice
    
    return amount
    












col=['symbol','price']

df= pd.DataFrame(columns=col)

mom=3
min_length=mom+1
print("Enter total capital to invest")
capital=float(input(">> "))



print("Pick a trading strategy\n 1.Moving average\n 2. Momentum \n 3.Mean Reversion")
print("type 1, 2 or 3")
val=int(input(">> "))

amount=capital











def run_momentum(df,mom=3,amount=amount):
    initial_amount=amount
    total=0
    min_length=mom+1
    units=0
    currentPosition=0
    trades=[]
    try:
        while True:
            data=socket.recv_string()
            sym,val=data.split(':')
            
            t=datetime.now()
            df_temp=pd.DataFrame(np.array([sym,val]).reshape(1,-1),columns=col,index=[t])
            
            df_temp['price']=pd.to_numeric(df_temp['price'])
            df=pd.concat([df,df_temp])
            
            dr=df.resample('5s',label='right').last()
            dr['returns']=np.log(dr['price']/dr['price'].shift(1))
            s="Neutral"    
            if (len(dr)<min_length):
                msg = "Retrieving data from server."
                for x in range(5):
                    msg = msg + "."
                    print(msg)
                    time.sleep(1)
                    os.system("cls")
            
            else:
                min_length+=1
                dr['momentum']=np.sign((dr['returns']).rolling(mom).mean())
                print('\n'+'='*51)
                print('NEW SIGNAL | time: {}'.format(datetime.now()))
                print('='*51)
                
                
                if dr['momentum'].iloc[-1]==1.0:
                    
                    if currentPosition == 1:
                        s="Neutral position"
                    
                    elif currentPosition == 0:
                    
                        s='LONG market position.\n'
                        total=amount
                        units=go_long(initial_amount,dr['price'].iloc[-1])
                        
                        trades.append(f"Bought {int(units)} ")
                    
                elif dr['momentum'].iloc[-1]==0:
                    if currentPosition==0:
                        s="Neutral position"
                        
                        
                        
                        
                    elif currentPosition==1:
                        amount=sell(units,dr['price'].iloc[-1])
                        total+=amount-initial_amount
                        initial_amount=amount
                        
                        trades.append(f"Sold {units} and amount recieved {amount}")
                        s='Sell market position.\n\n'   

                print("Current market position = >")    
                print(s+"\n")
                print(dr.iloc[-1,:])
                print("\n"+"<==>"*20+"\n")
                time.sleep(5)   
    except KeyboardInterrupt: 
            print("Simulation terminated successfully")   
            
            print("Amount= ", total) 
            print('|'.join(trades))
            print( f"percentage of profits={((amount-capital)/capital)*100}%" )
            
            
            
         
         
         
            
            
            
            
            

    
def run_sma(df,sma1=3,sma2=4,amount=amount):
    
    total=0
    i=0   
    initial_amount=amount
    currentPosition=0
    units=0
    trades=[]
    try: 
        while True:
                print("Use Ctrl-c to stop the simulation\n\n")
                
                data=socket.recv_string()
                sym,val=data.split(':')
                t=datetime.now()
                df_temp=pd.DataFrame(np.array([sym,val]).reshape(1,-1),columns=col,index=[t])
                
                df_temp['price']=pd.to_numeric(df_temp['price'])


                df=pd.concat([df,df_temp])
                s=""
            
                dr=df.resample('5s',label='right').last()
                dr['SMA1']=dr['price'].rolling(sma1).mean()
                dr['SMA2']=dr['price'].rolling(sma2).mean()
                
                if i>=sma2:
                    
                        if dr['SMA1'].iloc[i]>dr['SMA2'].iloc[i]:
                                if currentPosition==1:
                                    s="Neutral Positon"
                                    
                                elif currentPosition==0:
                                    total=amount
                                    units=go_long(initial_amount,dr['price'].iloc[-1])
                                    trades.append("Units bought = "+str(int(units))+" ")
                                    currentPosition=1
                                    s="Buy / Long position"
                          
                        if dr['SMA1'].iloc[i]<dr['SMA2'].iloc[i]:
                            if currentPosition==0:
                                s="neutral position"
                            
                            elif currentPosition==1:
                                s="Sell position"
                                amount=sell(units,dr['price'].iloc[-1])
                                
                                total+=amount-initial_amount
                                initial_amount=amount
                                trades.append("Units sold = "+str(int(units))+" Capital= "+str(amount))
                                currentPosition=0
                                units=0                     
                            
                
                print('NEW SIGNAL | time: {}'.format(datetime.now()))
                print('='*51)
        
                print("Recommended position => \n")
                print(s)
            
                print(dr.iloc[-1,:])
                print("\n"+"<==>"*20+"\n")
                time.sleep(5)   
                i+=1
                
                
                
    except KeyboardInterrupt:
            print("Simulation terminated successfully")   
            
            print("Amount= ", total) 
            print('|'.join(trades))
            print( f"percentage of profits={((amount-capital)/capital)*100}%")
            
            
            
            
            
            
            
            
  
    
    
def run_mean_reversion(df,threshold=0.25,sma=3,amount=amount):
    initial_amount=amount 
    i=0   
    total=0
    currentPosition=0
    units=0
    trades=[]
    try: 
        while True:
                print("Use Ctrl-c to stop the simulation\n\n")
                
                data=socket.recv_string()
                sym,val=data.split(':')

                t=datetime.now()
                df_temp=pd.DataFrame(np.array([sym,val]).reshape(1,-1),columns=col,index=[t])
                df_temp['price']=pd.to_numeric(df_temp['price'])
                s="Neutral"

                df=pd.concat([df,df_temp])
                
            
                dr=df.resample('5s',label='right').last()
                dr['SMA']=dr['price'].rolling(sma).mean()
                              
                if i>=sma:
                        if dr['price'].iloc[i]>dr['SMA'].iloc[i]+threshold:
                            
                            amount=sell(units,dr['price'].iloc[-1])
                            total+=amount-initial_amount
                            initial_amount=amount
                            currentPosition=0
                                
                            
                                
                        if dr['price'].iloc[i]<dr['SMA'].iloc[i]-threshold:
                            
                            
                            if currentPosition==1:
                                s="Neutral Positon"
                                    
                            elif currentPosition==0:
                                total=amount
                                units=go_long(amount,dr['price'].iloc[-1])
                                trades.append("Units bought = "+str(units)+" ")
                                currentPosition=1
                                s="Buy / Long position"
                                currentPosition=1
                               
                          
                
                print('NEW SIGNAL | time: {}'.format(datetime.now()))
                print('='*51)
                
                print("Recommended position => \n")
                print(s)
                
            
            
                print(dr.iloc[-1,:])
                print("\n"+"<==>"*20+"\n")
                time.sleep(5) 
                i+=1  
                
                
                
                
    except KeyboardInterrupt:
            print("Interrupted:")   
            print("Amount= ", total) 
            print('|'.join(trades))
            print( f"percentage of profits={((amount-capital)/capital)*100}%" )
            
            






     
            
df= pd.DataFrame(columns=col)    
if val==1:
    
    
    run_sma(df)
    
elif val==2:
    run_momentum(df=df)
else:
    run_mean_reversion(df)
    




    

        
    