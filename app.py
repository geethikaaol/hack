#!/usr/bin/env python

import urllib
import requests
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "runreport":
        return {}
    result = req.get("result")
    
    data = json.dumps(result.get("parameters"))
    baseurl = "http://ec2-204-236-199-93.compute-1.amazonaws.com:8080"
    headers = {'Content-Type': 'application/json'}
    
    r = requests.post(url=baseurl, data=data, headers=headers).content
    
    speech = "The result is" + r + "."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-reporting"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
