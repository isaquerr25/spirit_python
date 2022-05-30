import MetaTrader5 as mt5
import time

ea_magic_number = 9986989 # if you want to give every bot a unique identifier

def get_info(symbol):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolinfo_py
    '''
    # get symbol properties
    info=mt5.symbol_info(symbol)
    return info

def open_trade(action, symbol, lot, sl_points, tp_points, deviation):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # prepare the buy request structure
    selected=mt5.symbol_select(symbol,True)
    if not selected:
        print(f"Failed to select {symbol}, error code =",mt5.last_error())
    else:
        symbol_info = get_info(symbol)

        if action == 'buy':
            trade_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask
        elif action =='sell':
            trade_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
        point = mt5.symbol_info(symbol).point

        buy_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        # "sl": price - 100 * point,

        # "tp": price + 100 * point,

        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
            }
        # send a trading request

        result = mt5.order_send(buy_request)      
        return result, buy_request 

def close_trade(action, buy_request, result, deviation):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # create a close request
    # orders=mt5.orders_total()
    # buy_request = {}
    # for find_ordens in orders:
    #     if ticket_py = find_ordens.
    selected=mt5.symbol_select(symbol,True)
    if not selected:
        print(f"Failed to select {symbol}, error code =",mt5.last_error())
    else:
        symbol = buy_request['symbol']
        if action == 'buy':
            trade_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask
        elif action =='sell':
            trade_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
        position_id=result.order
        lot = buy_request['volume']

        close_request={
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": trade_type,
            "position": position_id,
            "price": price,
            "deviation": deviation,
            "magic": ea_magic_number,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        # send a close request
        result=mt5.order_send(close_request)


# This is how I would execute the order


def get_ticket_no(ticket):
    
    # get the list of positions on symbols whose names contain "*EUR*"
    symmbol_positions=mt5.positions_get()
    print('fo222222222222a')
    if symmbol_positions != None:
        print('forttewa')
        lst = list(symmbol_positions)
        print('fortttii7777a')
        for list_orders in lst:
            print('fora')
            if int(list_orders[0]) == int(ticket):
                print('dentro')
                return ticket
    return 0


# mt5.initialize()

# terminal_info_dict = mt5.terminal_info()._asdict()
# for prop in terminal_info_dict:
#     print("  {}={}".format(prop, terminal_info_dict[prop]))
    
# print('passou um')
# authorized = mt5.login(login=83000449, server="Exness-MT5Trial12",password="Peitoes97")


# terminal_info_dict = mt5.terminal_info()._asdict()


# for prop in terminal_info_dict:
#     print("  {}={}".format(prop, terminal_info_dict[prop]))

# time.sleep(45)
# print('passou 2')

# authorized = mt5.login(login=82019516, server="Exness-MT5Trial11",password="Peitoes97")


# terminal_info_dict = mt5.terminal_info()._asdict()
# for prop in terminal_info_dict:
#     print("  {}={}".format(prop, terminal_info_dict[prop]))
# get_ticket_no(175083)

# mt5.Close("AUDCADm",ticket=175083)


def get_ticket_return_list(ticket):
    
    # get the list of positions on symbols whose names contain "*EUR*"
    symmbol_positions=mt5.positions_get()
    if symmbol_positions==None:
        print("No positions with group=\"*EUR*\", error code={}".format(mt5.last_error()))    
    elif len(symmbol_positions)>0:
        lst = list(symmbol_positions)
        for list_orders in lst:
            if list_orders[0] == ticket:                
                return list_orders
    return 0


def close_trade_by_ticket(by_ticket):
    print(by_ticket)
    return (mt5.Close(by_ticket['par'] ,ticket= int(by_ticket['ticket']) ))
