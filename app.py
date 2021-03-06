#!/usr/bin/env python

import urllib
import json
import os

from urllib2 import urlopen
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
    parameters = result.get("parameters")
    date = parameters.get("date")

    baseurl = "http://ec2-204-236-199-93.compute-1.amazonaws.com:8080"
    url = "https://jsonplaceholder.typicode.com/posts"
    response = urlopen(baseurl,json.dumps(parameters)).read()
    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    speech = "The result for your query is :" + str(response)

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
