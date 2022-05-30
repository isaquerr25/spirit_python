from datetime import datetime
from socket import timeout
import MetaTrader5 as mt5
import asyncio
from API import open_trade, close_trade, get_ticket_no, close_trade_by_ticket
import requests
import json
import time
from request_graphql import run_graphql
from utils import create_Object
import traceback
local_mt = 'C:\Program Files\XM Global MT5/terminal64.exe'
print('load all')
ativite_change = ''
account_n =''
test = mt5.initialize(path=r''+local_mt, login=0, server='tes',password='tes')


query = """
{
  ordersFilterAccount(data:{
    local:["default","pato"]
  }){
    id
  	name
    server
    accountNumber
    allCurrent
    allCopyCurrent
    finishDate
    status
    typeAccount
    local
    password
    missingOrders{
      id
      status
      ordersId
      ticket
      par
      direction
      lote
      local
      type
      accountMetaTraderId
    }
  }
}
"""


while True:
    time.sleep(5)
    
    try:
        
        
        fd = run_graphql(query,'query')
        if fd:
            print('s')
            ativite_change = fd
         
            for profile in fd['data']['ordersFilterAccount']:
                print(profile)
                
                
                try:
                    print('get information DB')
                    
                    if account_n != profile['accountNumber']:
                        
                        account_n = profile['accountNumber']
                        print('account_n:>',account_n)

                        authorized = mt5.initialize(path=r''+local_mt ,
                            login=account_n, server=profile['server'],password=profile['password'],timeout=25000)
                    
                    if authorized:
                        ordersAccountGroupDefinition = { 
                        "data":[]
                        }
                        
                        
                        
                        if profile['missingOrders']:
                            for orders in profile['missingOrders']:
                                print('pre order :::> ',orders['direction'], orders['par'], float(orders['lote'])/100,0, 0, 10)
                                result, buy_request = open_trade(orders['direction'], orders['par'], float(orders['lote'])/100,0, 0, 10)

                                if(orders['status'] == 'OPEN'):

                                    if result != None:
                                        ordersAccountGroupDefinition['data'].append(create_Object(result,orders,'OPEN'))

                                elif(orders['status'] == 'CLOSE'): 

                                    if get_ticket_no(int( orders['ticket'])) !=0:

                                        result = close_trade_by_ticket(orders)
                                        print('result  ',result)
                                        print('------------------------------------------------------  ')
                                        if result:
                                                
                                            ordersAccountGroupDefinition['data'].append(create_Object(result,orders,'CLOSE'))
                                            print('rsdfsdfsdultsdf  ')
                            result = run_graphql(
                                f""" mutation
                                {'{'}
                                    ordersAccountGroupDefinition(
                                    {ordersAccountGroupDefinition}
                                    ){'{'}
                                        field
                                        message
                                    {'}'}
                                {'}'}
                                """,'mutation')
                            print('result   ',result)
                        safe = 5

                    else:
                        #FIXME report is wrong login
                        print("failed to connect at account #{}, error code: {}",mt5.last_error())

                except Exception as inst:
                    traceback.print_exc()
                    print('E111rro ',inst)
    except Exception as inst:
        print('Erro ',inst)

