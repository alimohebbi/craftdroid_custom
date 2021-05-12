import requests


def send_object(math_object):
    # run w2v_service.py first to activate the w2v service
    resp = requests.post(url='http://127.0.0.1:5000/ranking', json=math_object).json()
    return resp
