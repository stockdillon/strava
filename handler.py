import os
import json
print("hello world")
# print(os.environ)

clientId = os.environ.get('CLIENT_ID')
clientSecret = os.environ.get('CLIENT_SECRET')
refreshToken = os.environ.get('REFRESH_TOKEN')

print(f'client_id: {clientId}')
print(f'clientSecret: {clientSecret}')
print(f'refreshToken: {refreshToken}')


authUrl = f'https://www.strava.com/oauth/authorize?client_id={clientId}&redirect_uri=http://localhost&response_type=code&scope=activity:read_all'

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': clientId,
    'client_secret': clientSecret,
    'refresh_token': refreshToken,
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
res = requests.get(activites_url, headers=header, params=param)
my_dataset = requests.get(activites_url, headers=header, params=param).json()

data = json.loads(res.text)
# print(data)
# badge names, time, type
for k,v in data[0].items():
    print(k)
for activity in data:
    print(activity['name'])
print(json.dumps(data))
# print(my_dataset[0]["name"])
# print(my_dataset[0]["map"]["summary_polyline"])