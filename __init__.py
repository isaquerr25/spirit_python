from request_graphql import getInfoDef, setOrders, setWrongAuthorized, getPlanInvoice


for item in getPlanInvoice('pato'):
    print(item['PlanInvoices'])
    print(item['AccountMetaTrader'])
