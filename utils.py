def creat_Object(type_use,result={},f_ordes={}):
    order_process = {}
    print(f_ordes)
    if type_use=="sucess_open":
        order_process = {
                            "ticket": result.order,
                            "direction": f_ordes['direction'],
                            "lote":f_ordes['lote'],
                            "ticket_old":f_ordes['ticket'],
                            "status":"abertura"
                        }
    elif type_use=="erro_open":
        order_process = {
                            "ticket":0,
                            "direction": f_ordes['direction'],
                            "lote":f_ordes['lote'],
                            "ticket_old":f_ordes['ticket'],
                            "status":"err"
                        }
    elif type_use=="sucess_close":
        order_process = {
                        "ticket":f_ordes['ticket'],
                        "direction": f_ordes['direction'],
                        "lote":f_ordes['lote'],
                        "ticket_old":f_ordes['ticket_old'],
                        "status":"fechamento"
                    }
    else:
        order_process = {
                        "ticket":f_ordes['ticket'],
                        "direction": f_ordes['direction'],
                        "lote":f_ordes['lote'],
                        "ticket_old":f_ordes['ticket_old'],
                        "status":"err"
                    }
    return(order_process)