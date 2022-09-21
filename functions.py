from datetime import datetime
import requests
import re

def user_agent():
    headers = {
        'User-Agent': "sp3-bot Discord Bot (Github: zian999)".encode()
    }
    return headers

def get_schedule(p1, p2):
    url = "https://spla3.yuu26.com/api/"
    res = requests.get(f"{url}{p1}/{p2}", headers=user_agent())
    if res.status_code == 200:
        data = res.json()
        return data['results']
    else:
        data = None
        return data

# def get_now(p1):
#     return get_schedule(p1, 'now')

# def get_next(p1):
#     return get_schedule(p1, 'next')

def handle(entry):
    st = datetime.strptime(entry['start_time'], "%Y-%m-%dT%H:%M:%S%z")
    et = datetime.strptime(entry['end_time'], "%Y-%m-%dT%H:%M:%S%z")
    rule_name = entry['rule']['name']
    if 'stages' in entry:
        stages = [s['name'] for s in entry['stages']]
        return [[st, et], rule_name, stages]
    if 'weapons' in entry:
        weapons = [w['name'] for w in entry['weapons']]
        stage = entry['stage']['name']
        return [[st, et], stage, weapons]

def timediff(earlier_time, later_time):
    s = str(later_time - earlier_time).split(':')
    if len(s[0]) > 3:
        dayhour = s[0].split(' days, ')
        s.insert(0, dayhour[0])
        s[1] = dayhour[1]
    else:
        s.insert(0, '0')
    s[3] = str(round(float(s[3]), 1))
    return s
