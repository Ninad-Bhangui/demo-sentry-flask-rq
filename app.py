import os
from flask import Flask
from redis import Redis
from rq import Queue

from jobs import broken_function

import sentry_sdk
from sentry_sdk.integrations.rq import RqIntegration
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(os.environ['SENTRY_DSN'], integrations=[FlaskIntegration(), RqIntegration()])

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/error')
def error():
    return 1/0

@app.route('/enqueue')
def enqueue():
    q = Queue(connection=Redis())
    result = q.enqueue(broken_function, "Error within RQ job.")
    return "queued"

if __name__ == "__main__":
    app.run()
