def create_Object(ticket,f_orders={},statusCurrent=''):
    order_process = {}
    print(f_orders)

    order_process = {
        "id": None if statusCurrent =='OPEN' else f_orders['id'],
        "ordersId":f_orders['ordersId'],
        "par":f_orders['par'],
        "ticket":ticket,
        "direction": f_orders['direction'],
        "lote":f_orders['lote'],
        "ticket_old":f_orders['ticket_old'],
        "status":statusCurrent,
        "local":f_orders['local'],
        "type":f_orders['type'],
        "accountMetaTraderId":f_orders['accountMetaTraderId'],
        }
    return(order_process)