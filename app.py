from flask import Flask, Response
from requests import get

app = Flask(__name__)
SITE_NAME = 'https://www.strava.com/api/v3'
# clientId = os.environ.get('CLIENT_ID')
# clientSecret = os.environ.get('CLIENT_SECRET')
# refreshToken = os.environ.get('REFRESH_TOKEN')
token = "ba145767d650c1bdd219342f579744a62198aa2d"
headers = {"Authorization": f"Bearer {token}"}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    res = get(f'{SITE_NAME}/{path}', headers=headers)
    # return res.text
    resp = Response(res.text)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp    

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
