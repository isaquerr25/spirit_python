def create_Object(orderCreate,f_orders={},statusCurrent=''):
    order_process = {}
    print('orderCreate   >>>', orderCreate)
    print(f_orders)

    order_process = {
        'id': None if statusCurrent =='OPEN' else f_orders['id'],
        'ordersId':f_orders['ordersId'],
        'par':f_orders['par'],
        'ticket':orderCreate.order,
        'direction': f_orders['direction'],
        'lote':f_orders['lote'],
        'status':statusCurrent,
        'local':f_orders['local'],
        'type':f_orders['type'],
        'accountMetaTraderId':f_orders['accountMetaTraderId'],
        }
    print('order_process  ______))))____>',order_process)
    return(order_process)
