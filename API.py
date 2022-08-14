import MetaTrader5 as mt5
import time
import json
import traceback
with open('env.json') as json_file:
    envFile = json.load(json_file)


def get_info(symbol):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolinfo_py
    '''
    # get symbol properties
    info = mt5.symbol_info(symbol)
    return info


def open_trade(action, symbol, lot, sl_points, tp_points, deviation):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # prepare the buy request structure
    print('000000000')
    selected = mt5.symbol_select(symbol, True)
    if not selected:
        print(f"Failed to select {symbol}, error code =", mt5.last_error())

        return 'error symbol', None
    else:
        print('entro')
        try:
            price = mt5.symbol_info_tick(symbol).ask

            buy_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY if action == 'BUY' else mt5.ORDER_TYPE_SELL,
                "price": price,
                "deviation": deviation,
                "magic": envFile['magicNumber'],
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
            }

            result = mt5.order_send(buy_request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("order_send failed, retcode={}".format(result.retcode))
                return None, None
            else:
                return result, buy_request

        except Exception as inst:
            traceback.print_exc()
            print(inst)
            return None, None


def close_trade(ticket, symbol):
    print('close_trade')
    if(mt5.orders_get(ticket=ticket) is None):
        return True
    result = mt5.Close(symbol, ticket=ticket)
    print(result)
    if not result:
        print("orderClose failed, retcode={}".format(ticket))
        return None
    else:
        return result

# This is how I would execute the order


def get_ticket_no(ticket):

    # get the list of positions on symbols whose names contain "*EUR*"
    symmbol_positions = mt5.positions_get()
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
    symmbol_positions = mt5.positions_get()
    if symmbol_positions == None:
        print("No positions with group=\"*EUR*\", error code={}".format(mt5.last_error()))
    elif len(symmbol_positions) > 0:
        lst = list(symmbol_positions)
        for list_orders in lst:
            if list_orders[0] == ticket:
                return list_orders
    return 0


def close_trade_by_ticket(by_ticket):
    print(by_ticket)
    return (mt5.Close(by_ticket['par'], ticket=int(by_ticket['ticket'])))
