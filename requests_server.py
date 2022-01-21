import requests
import json
ip_location = 'http://localhost:8000'

def server_inform():
    send ={
            "server": "set_01"
        }
    # return(requests.post(ip_location+'/api/set_sinal',data = send))
    return(requests.get(ip_location+'/ordenscorrent/manager/vps_01'))

def server_status(send):
    
    gf = requests.post(ip_location+'/ordenscorrent/set_sinal_reference',data=json.dumps(send), headers={'content-type': 'application/json'} )
    return(gf.json())


def server_err_enter_account(account_co,msn):
    
    send = {
        "account":account_co,
        "status":str(msn)
    }

    return(requests.post(ip_location+'/userk/information_account',data=json.dumps(send), headers={'content-type': 'application/json'}))
    
    