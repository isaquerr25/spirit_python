from gql.transport.aiohttp import AIOHTTPTransport
from gql import Client, gql
import os
import json
import traceback
envFile = ''
with open('env.json') as json_file:
    envFile = json.load(json_file)


transport = AIOHTTPTransport(url=envFile['addressApi'])
client = Client(transport=transport, fetch_schema_from_transport=True)
query = gql(
    """
    query OrdersFilterAccount($data:ObjectFilterAccountOrders!) {
      ordersFilterAccount(data:$data)
      {
        id
        password
        server
        accountNumber
        missingOrders{
          id
          ordersId
          ticket
          par
          direction
          lote
          local
          type
          accountMetaTraderId
          status
        }
      }
    }
    """
)

mutation = gql(
    """
    mutation OrdersAccountGroupDefinition($data:[InputOrdersAccountGroupDefinition!]!) {
        ordersAccountGroupDefinition(data:$data)
        {
            field
            message
        }
    }
    """
)


planInvoiceLocalPython = gql(
    """
    query PlanInvoiceLocalPython($data:[String!]!) {
        planInvoiceLocalPython(
            data: {
        local:$data
        }){
            id
            status
            PlanInvoices{
                id
                beginDate
                finishDate
                realDollarQuote
                local
                status
                type
                grossProfitDollar
                createdAt
            
            }
            AccountMetaTrader{
                id
                name
                password
                accountNumber
                server
                local
            }
        }
    }
    """
)

invoiceCreateStaff = gql(
    """
    mutation InvoiceCreateStaff($idPlanToAccount:Int,$accountNumber:Int,$profit:Int!,$capital:Int!,$planInvoicesId:Int) {
        invoiceCreateStaff(
		res: {
            idPlanToAccount:$idPlanToAccount
			accountNumber: $accountNumber
			profit: $profit
			capital: $capital
			planInvoicesId: $planInvoicesId
		}
	) {
		field
		message
	    }
    }
    """
)


glqSetWrongAuthorized = gql(
    """
    query AccountUpdatePython($data:InputAccountPython!) {
        accountUpdatePython(data:$data)
        {
            field
            message
        }
    }
    """
)


# get all info need in server

def getInvoiceCreateStaff(idPlanToAccount, accountNumber, profit, capital, planInvoicesId):
    try:
        result = client.execute(invoiceCreateStaff, variable_values={
            "idPlanToAccount": idPlanToAccount,
            "accountNumber": accountNumber,
            "profit": profit,
            "capital": capital,
            "planInvoicesId": planInvoicesId,
        })
        return result
    except:
        print('getPlanInvoice error')
        traceback.print_exc()
        return None


def getPlanInvoice(info):
    try:
        result = client.execute(planInvoiceLocalPython, variable_values={
            "data": info
        })
        return result['planInvoiceLocalPython']
    except:
        print('getPlanInvoice error')
        traceback.print_exc()
        return None


def getInfoDef():
    try:
        result = client.execute(query, variable_values={
            "data": envFile['localReference']})
        return result
    except:
        print('getInfoDef error')
        traceback.print_exc()
        return None

# send order to db


def setOrders(data):
    try:
        result = client.execute(mutation, variable_values={
            "data": data})
        return result
    except:
        print('setOrders error')
        traceback.print_exc()
        return None


def setWrongAuthorized(data):
    try:
        result = client.execute(glqSetWrongAuthorized, variable_values={
            "data": data})
        return result
    except:
        print('setOrders error')
        traceback.print_exc()
        return None


# Scheme to send to create new order in db
# data = [{'id': None, 'ordersId': 38, 'par': 'XAUUSD', 'ticket': 15611515, 'direction': 'BUY', 'lote': 10,
#        'status': 'OPEN', 'local': 'default', 'type': 'NORMAL', 'accountMetaTraderId': 7}]

#
# getInfoDef()

# setOrders(data)
