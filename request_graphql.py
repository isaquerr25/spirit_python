request_url = 'http://localhost:4000/graphql' 

graphql_query = """{
  ordersFilterAccount(data:{
    local:["default","pato"]
  }){
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
}"""


# An example to get the remaining rate limit using the Github GraphQL API.

import requests

headers = {"Authorization": "Bearer YOUR API KEY"}


def run_graphql(query,type): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('http://localhost:4000/graphql', json={type: query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
query = """
{
  ordersFilterAccount(data:{
    local:["default","pato"]
  }){
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
      status
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
mutation = """
  mutation{
    ordersAccountGroupDefinition(data:[
        {
          id: null,
          status: OPEN,
          ordersId: 1,
          ticket: 10132310,
          par: "XAUUSD",
          direction: BUY,
          lote: 10,
          local: "default",
          type: NORMAL,
          accountMetaTraderId: 2
        }
        {
          id: 3,
          status: CLOSE,
          ordersId: 1,
          ticket: 100000,
          par: "XAUUSD",
          direction: BUY,
          lote: 10,
          local: "default",
          type: NORMAL,
          accountMetaTraderId: 2
        }
    ]){
      field
      message
    }
  }
"""




