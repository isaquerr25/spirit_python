import numpy as np
import pandas as pd
from datetime import datetime
import MetaTrader5 as mt5
import asyncio
from API import open_trade, close_trade

print('passo')

authorized = mt5.initialize(login=82019516, server="Exness-MT5Trial11",password="Peitoes97")
print('2')

# authorized=mt5.login(account)  # the terminal database password is applied if connection data is set to be remembered
if authorized:
    print("connected to account #{}".format(authorized))
    
# symbol = "AUDCHFm"
# symbol_info = mt5.symbol_info(symbol)

# result, buy_request = open_trade('buy', 'AUDCADm', 0.01, 0, 0, 10)

# print(result.order,result.volume)
# print("failed to connect at account #{}, error code: {}",mt5.last_error())
orders=mt5.positions_get()

lst = list(orders)
print("Orders noasdas  " ,lst)

# close_trade('buy', buy_request, result, 10)
orders=mt5.orders_get(group="*AUD*")
if orders is None:
    print("No orders on GBPUSD, error code={}".format(mt5.last_error()))
else:
    print("Total orders on GBPUSD:",len(orders))
    # display all active orders
    for order in orders:
        print(order)

def gf():
    symbol = "AUDCADm"
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()
    
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            quit()

    lot = 0.1
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
        