import time
import MetaTrader5 as mt5

def init():
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()


# prepare the buy request structure
lott = 0.15
symboll = "EURUSD"

deviation = 20
magic = 987654321

def buy():
    # establish connection to the MetaTrader 5 terminal
    init()
    
    symbol = symboll
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

    lot = lott
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 1000 * point,
        "tp": price + 1000 * point,
        "deviation": deviation,
        "magic": magic,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
        mt5.shutdown()
        quit()
 
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))
    print("   sleep 2 seconds before closing position #{}".format(result.order))


def close(ticket_no):
    init()
    symbol = symboll
    symbol_info = mt5.symbol_info(symbol)
    lot = lott
    # create a close request
    position_id=ticket_no
    price=mt5.symbol_info_tick(symbol).bid
    deviation=20
    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": magic,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a trading request
    result=mt5.order_send(request)
    # check the execution result
    print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("4. order_send failed, retcode={}".format(result.retcode))
        print("   result",result)
    else:
        print("4. position #{} closed, {}".format(position_id,result))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    
    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
    quit()


def get_ticket_no():
    init()
    symbol = symboll
    symbol_info = mt5.symbol_info(symbol)
    
    positions=mt5.positions_get(symbol=symbol)
    if positions==None:
        print("No positions on EURUSD, error code={}".format(mt5.last_error()))
    elif len(positions)>0:
        print("Total positions on EURUSD =",len(positions))
        # display all open positions
        for position in positions:
            print(position)

    # get the list of positions on symbols whose names contain "*EUR*"
    symmbol_positions=mt5.positions_get()
    if symmbol_positions==None:
        print("No positions with group=\"*EUR*\", error code={}".format(mt5.last_error()))    
    elif len(symmbol_positions)>0:
        lst = list(symmbol_positions)
        ticket_no = lst[0][0] # get the ticket number
        magic_no = lst[0][6] # get the magic number
        print(f'{ticket_no=}')
        print(f'{magic_no=}')
        return ticket_no

    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
    quit()


def get_magic_no():
    init()
    symbol = symboll
    symbol_info = mt5.symbol_info(symbol)
    
    positions=mt5.positions_get(symbol=symbol)
    if positions==None:
        print("No positions on EURUSD, error code={}".format(mt5.last_error()))
    elif len(positions)>0:
        print("Total positions on EURUSD =",len(positions))
        # display all open positions
        for position in positions:
            print(position)

    # get the list of positions on symbols whose names contain "*EUR*"
    symmbol_positions=mt5.positions_get()
    if symmbol_positions==None:
        print("No positions with group=\"*EUR*\", error code={}".format(mt5.last_error()))    
    elif len(symmbol_positions)>0:
        lst = list(symmbol_positions)
        ticket_no = lst[0][0] # get the ticket number
        magic_no = lst[0][6] # get the magic number
        print(f'{ticket_no=}')
        print(f'{magic_no=}')
        return magic_no

    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
    quit()
    

def close_order():
    if get_magic_no() == magic:
        close(get_ticket_no())
    else:
        print("Order not found!")
    
    
buy()
time.sleep(2)
close_order()