import uuid
import logging
from flask_redis import FlaskRedis
from flask import Flask, request, render_template

app = Flask(__name__)
redis_client = FlaskRedis(app)

redis_client.set('potato', 'tomato')

@app.route('/')
def index():
    return redis_client.get('potato')

if __name__ == "__main__":
    app.debug = True
    logging.getLogger().setLevel("DEBUG")
    app.run(host="0.0.0.0", port=80)
