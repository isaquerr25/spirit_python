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
        name
        server
        accountNumber
        allCurrent
        allCopyCurrent
        finishDate
        status
        typeAccount
        local
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


def getInfoDef():
    try:
        result = client.execute(query, variable_values={
            "data": envFile['localReference']})
        print(result)
        return result
    except:
        traceback.print_exc()
        return None


def setOrders(data):
    try:
        result = client.execute(mutation, variable_values={
            "data": data})
        print(result)
        return result
    except:
        print('setOrders error')
        traceback.print_exc()
        return None


data = [{'id': None, 'ordersId': 38, 'par': 'XAUUSD', 'ticket': 15611515, 'direction': 'BUY', 'lote': 10,
        'status': 'OPEN', 'local': 'default', 'type': 'NORMAL', 'accountMetaTraderId': 7}]


getInfoDef()
setOrders(data)
