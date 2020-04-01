import json

import re
import requests
from bs4 import BeautifulSoup
from datetime import date,timedelta,datetime

def dates():
    time = datetime.now().time()
    hr = int(str(time)[:2])
    if hr > 10:
        dates = datetime.today()
    else:
        dates = datetime.today() - timedelta(days=1)
    s = str(dates)
    s = s.split()
    return s[0]


    
def globally(data):
    url = "https://ncov2019.live"
    response = requests.get(url)

    res = BeautifulSoup(response.content, "html.parser")
    mydivs1 = res.findAll("p")
    for j in range(-2, -12, -2):
        key = mydivs1[j].text.strip()
        val = mydivs1[j - 1].text.strip()
        data[key] = val

    score = res.find(text=re.compile('India'))
    scores = score.parent.parent.findAll('td')
    for iid, tg in enumerate(scores):
        if iid == 3:
            data['Change in Admitted'] = tg.text.strip()
        if iid == 6:
            data['Change in Death'] = tg.text.strip()
            break
    return data


def stripper(a):
    return int(re.sub('[^0-9]+', '', a.text.strip()))


def graph():
    url = "https://www.mohfw.gov.in/"
    response = requests.get(url)
    res = BeautifulSoup(response.content, "html.parser")
    mydivs1 = res.findAll('tbody')

    mydivs = mydivs1[-1]
    conCase, cureCase, deathCase, total = dict(), dict(), dict(), dict()
    tdiv = mydivs.findAll('tr')
    for td in tdiv:
    	val = td.findAll('td')
    	if len(val)==5:
    		# print(val)
    		# print('=======================')
    		key = val[1].text.strip()
    		
    		conCase[key] = stripper(val[2])
    		if stripper(val[3]) != 0:
    			cureCase[key] = stripper(val[3])
    		if stripper(val[4]) != 0:
    			deathCase[key] = stripper(val[4])
    	else:
            total['conCase'] = stripper(val[1])
            total['cured'] = stripper(val[2])
            total['death'] = stripper(val[3])
            break

    return [conCase, cureCase, deathCase, total]


def main():
    data = dict()
    data = globally(data)

    with open('./static/json/data.json', 'w') as fp:
        json.dump(data, fp)

    return
