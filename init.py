from datetime import datetime
from socket import timeout
import MetaTrader5 as mt5
import asyncio
from API import open_trade, close_trade, get_ticket_no, close_trade_by_ticket
import requests
import json
import time
from request_graphql import getInfoDef, setOrders, setWrongAuthorized
from utils import create_Object
from cashIn import workCashIn
import traceback
local_mt = 'C:\Program Files\MetaTrader5-1/terminal64.exe'
print('load all')
ativite_change = ''
account_n = ''
test = mt5.initialize(path=r''+local_mt, login=0, server='tes', password='tes')
print('connect,', test)
envFile = ''
with open('env.json') as json_file:
    envFile = json.load(json_file)

while True:
    time.sleep(5)
    workCashIn(mt5, envFile['addressApi'], local_mt)
    try:

        fd = getInfoDef()
        print('all information ++>> ', fd)
        if fd:
            print('s')
            ativite_change = fd
            data = []
            for profile in fd['ordersFilterAccount']:
                print(profile)

                try:
                    print('get information DB')

                    if account_n != profile['accountNumber']:

                        account_n = profile['accountNumber']
                        print('account_n:>', account_n)

                        authorized = mt5.initialize(path=r''+local_mt,
                                                    login=account_n, server=profile['server'], password=profile['password'], timeout=25000)

                    if authorized:

                        if profile['missingOrders']:
                            for orders in profile['missingOrders']:
                                print('pre order :::> ', orders['direction'], orders['par'], float(
                                    orders['lote'])/100, 0, 0, 10)

                                if(orders['status'] == 'OPEN'):

                                    result, buy_request = open_trade(
                                        orders['direction'], orders['par'], float(orders['lote'])/100, 0, 0, 10)

                                    if result == 'error symbol':
                                        setWrongAuthorized(
                                            {'id': profile['id'], 'status': 'NOT_HAVE_ORDER_NAME_LOCAL_REFERENCE'})

                                    elif result is not None:
                                        data.append(create_Object(
                                            result, orders, 'OPEN'))

                                elif(orders['status'] == 'CLOSE'):

                                    if get_ticket_no(int(orders['ticket'])) != 0:

                                        result = close_trade(
                                            orders['ticket'], orders['par'])
                                        print(' result close  ', result)
                                        print(
                                            '------------------------------------------------------  ')
                                        if result is not None:

                                            data.append(orders)
                                            print('rsdfsdfsdultsdf  ')
                                    else:
                                        data.append(orders)
                    else:
                        # FIXME report is wrong login
                        setWrongAuthorized(
                            {'id': profile['id'], 'status': 'ERROR_LOGIN'})
                        print(
                            "failed to connect at account #{}, error code: {}", mt5.last_error())

                except:
                    traceback.print_exc()
                    print('except init')
            print('data server ', data)
            result = setOrders(data)

            print('Result server ', result)
    except Exception as inst:

        print('Erro ', inst)
