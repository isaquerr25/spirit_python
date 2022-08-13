from request_graphql import getInfoDef, setOrders, setWrongAuthorized, getPlanInvoice
import datetime


def workCashIn(mt5, local, local_mt):
    for item in getPlanInvoice(local):
        print(item['PlanInvoices'])
        print(item['AccountMetaTrader'])

        authorized = mt5.initialize(
            path=r''+local_mt,
            login=item['AccountMetaTrader']['accountNumber'],
            server=item['AccountMetaTrader']['server'],
            password=item['AccountMetaTrader']['password'],
            timeout=25000
        )

        from_date = datetime.strptime(item['PlanInvoices']['beginDate'])
        to_date = datetime.strptime(item['PlanInvoices']['finishDate'])
        history_orders = mt5.history_orders_total(from_date, to_date)
        if history_orders > 0:
            print("Total history orders=", history_orders)
        else:
            print("Orders not found in history")
