from request_graphql import getPlanInvoice
from datetime import datetime
import json
with open('env.json') as json_file:
    envFile = json.load(json_file)


def workCashIn(mt5, local, local_mt):
    print('------------------------------------------------------rodo--------------------------------------------------------')
    print('getPlanInvoice=>', getPlanInvoice(local))
    for item in getPlanInvoice(local):
        print(item['PlanInvoices'])
        print(item['AccountMetaTrader'])
        print('PlanInvoices=>',
              (item['PlanInvoices']['beginDate']).split('T')[0])
        from_date = datetime.strptime(
            (item['PlanInvoices']['beginDate']).split('T')[0], "%Y-%m-%d")
        to_date = datetime.strptime(
            (item['PlanInvoices']['finishDate']).split('T')[0], "%Y-%m-%d")

        authorized = mt5.initialize(
            path=r''+local_mt,
            login=item['AccountMetaTrader']['accountNumber'],
            server=item['AccountMetaTrader']['server'],
            password=item['AccountMetaTrader']['password'],
            timeout=25000
        )

        history_orders = mt5.history_orders_total(from_date, to_date)
        if history_orders > 0:
            print("Total history orders=", history_orders)
        else:
            print("Orders not found in history")

        print(from_date, to_date)
        deals = mt5.history_deals_get(from_date, to_date)

        if deals == None:
            print("No deals, error code={}".format(mt5.last_error()))

        elif len(deals) > 0:

            valueProfit = 0
            for x in deals:

                if x.magic == envFile['magicNumber']:
                    valueProfit += x.profit
                    print('Item => ', x.profit)
            print('valueProfit => ', valueProfit)
