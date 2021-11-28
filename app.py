from flask import Flask, Response, jsonify
from requests import get
from activities import ActivitiesResponseElement

app = Flask(__name__)
SITE_NAME = 'https://www.strava.com/api/v3'
# clientId = os.environ.get('CLIENT_ID')
# clientSecret = os.environ.get('CLIENT_SECRET')
# refreshToken = os.environ.get('REFRESH_TOKEN')
token = "42c9719a0e8349e0af670a8ea4c8874f22557740"
headers = {"Authorization": f"Bearer {token}"}
ONE_DAY_CACHE = 24 * 60 * 60

def getPhotoUrls(activity_id):
    resp = get(f'{SITE_NAME}/activities/{activity_id}', headers=headers)
    return resp.json()['photos']['primary']['urls']['600']

def setPhotoUrls(activity: ActivitiesResponseElement):
    id = activity.get('id')
    resp = get(f'{SITE_NAME}/activities/{id}', headers=headers)
    photo_url = resp.json()['photos']['primary']['urls']['600']
    activity['photo_url'] = photo_url

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    res = get(f'{SITE_NAME}/{path}', headers=headers)
    # return res.text
    resObj = res.json()
    # ids = list(map(lambda x: x.get('id'), resObj))
    ids = [x.get('id') for x in resObj if x.get('total_photo_count') > 0]
    # photos = [x for x in map(lambda x: getPhotoUrls(x), ids) if x is not None]
    photos = list(map(lambda x: getPhotoUrls(x), ids))
    for activity in [activity for activity in resObj if activity.get('total_photo_count') > 0]:
        # if not activity.get('total_photo_count') > 0:
        #     continue
        setPhotoUrls(activity)
    resp = jsonify({'activities': resObj})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Cache-Control'] = f'max-age={ONE_DAY_CACHE}'        
    return resp    

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
