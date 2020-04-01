import requests
import json
import os
from flask import current_app as app
from datetime import datetime


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    return


def data_indian():
	try:
		url = "https://api.covid19india.org/data.json"
		response = requests.get(url)
		data = response.json()
		with open('./static/json/time_series.json', 'w') as fp:
		    json.dump(data['cases_time_series'], fp)

		with open('./static/json/statewise.json', 'w') as fp:
		    json.dump(data['statewise'], fp)

		return data
	except Exception as inst:
		print(type(inst))
		print(inst.args)
		print(inst)

def data_global():
	try:
		url = "https://corona.lmao.ninja/all"
		response = requests.get(url)
		data = response.json()
		with open('./static/json/global_data.json', 'w') as fp:
		    json.dump(data, fp)
		return data
	except Exception as inst:
		print(type(inst))
		print(inst.args)
		print(inst)


def timer():
	curr_time = datetime.now().minute
	if curr_time%15==0:
		data_indian()
		data_global()
	return curr_time%15


def data_generaion(paths):
    filename = os.path.join(app.static_folder, 'json', paths)
    with open(filename) as fp:
        data = json.load(fp)
    return data

# timer()
# jprint(data_indian())
# jprint(data_global())