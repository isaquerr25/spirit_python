import numpy as np
import pandas as pd
from datetime import datetime
import MetaTrader5 as mt5
import asyncio
from API import open_trade, close_trade, get_ticket_no, close_trade_by_ticket
import requests
import json
import time
from utils import creat_Object
from requests_server import server_inform, server_status, server_err_enter_account

ativite_change = ''
while True:
    time.sleep(5)
    
    try:
        
    
        fd = server_inform()
        if ativite_change == fd.json():
            continue

        if fd:
            
            ativite_change = fd.json()
            print(ativite_change)
            for profile in fd.json()['base']:
                server_err_enter_account(profile['account'],'work')
                print('get information DB')
                
                authorized = mt5.initialize(login=profile['account'], server=profile['server_meta'],password=profile['password'])
                
                if authorized:
                    
                    ordens_enter = { 
                        "account":profile['account'], 
                        "open":{
                            "ordens_sucess" : [], 
                            "ordens_invalid" : []
                        },
                        "close":{
                            "ordens_sucess" : [], 
                            "ordens_invalid" : []
                        }
                    }
                    
                    
                    if profile['items']['open']:
                        for ordes in profile['items']['open']:

                            result, buy_request = open_trade(ordes['direction'], ordes['par'], float(ordes['lote']),0, 0, 10)

                            if result != None:
                                
                                ordens_enter['open']['ordens_sucess'].append(creat_Object("sucess_open",result,ordes))
                                
                            else:
                                ordens_enter['open']['ordens_invalid'].append(creat_Object("err_open",{},ordes))
                    
                    if profile['items']['close']:
                        
                        for ordes in profile['items']['close']:
                            print('fechar')
                            print(ordes['ticket'])
                            if get_ticket_no(int( ordes['ticket'])) !=0:

                                result = close_trade_by_ticket(ordes)
                                print('result  ',result)
                                print('------------------------------------------------------  ')
                                if result:
                                        
                                    ordens_enter['close']['ordens_sucess'].append(creat_Object("sucess_close",result,ordes))
                                    
                                else:
                                    print('rsdfsdfsdultsdf  22222222222222222222')
                                    ordens_enter['close']['ordens_invalid'].append(creat_Object("err_close"),result,ordes)
                            else:
                                print('rsdfsdfsdultsdf  ')
                                ordens_enter['close']['ordens_sucess'].append(creat_Object("sucess_close",{},ordes))
                                
                    safe = 5
                    while True:
                        print(ordens_enter)
                        new_server_status = server_status(ordens_enter)
                        print(new_server_status)
                        if (new_server_status != None and new_server_status != "err"):
                            break
                        
                        safe +=1
                        time.sleep(safe)
                else:
                    
                    server_err_enter_account(profile['account'],str("failed to connect at account #{}, error code: {}"+str(mt5.last_error())))
                    print("failed to connect at account #{}, error code: {}",mt5.last_error())
    except:
        pass

