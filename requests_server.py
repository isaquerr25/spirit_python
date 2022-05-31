import requests
import json
ip_location = 'http://localhost:8000'


def server_inform():
    send = {
        "vps_name": "set_01",
        "multipla": "1.5",
        "id_order": "aud"
    }
    # return(requests.post(ip_location+'/api/set_sinal',data = send))
    gf = requests.post(ip_location+'/ordenscorrent/manager/vps_01',
                       data=json.dumps(send), headers={'content-type': 'application/json'})
    return(gf)


def server_status(send):

    gf = requests.post(ip_location+'/ordenscorrent/set_sinal_reference',
                       data=json.dumps(send), headers={'content-type': 'application/json'})
    return(gf.json())


def server_err_enter_account(account_co, msn):

    send = {
        "account": account_co,
        "status": str(msn)
    }

    return(requests.post(ip_location+'/userk/information_account', data=json.dumps(send), headers={'content-type': 'application/json'}))
