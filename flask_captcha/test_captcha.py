
import uuid
import logging
#import unittest
from flask_session_captcha import  FlaskSessionCaptcha

from flask import Flask, request, render_template


from flask import Flask, request
from flask_sessionstore import Session
#from werkzeug.test import Headers

app = Flask(__name__)
app.config["SECRET_KEY"] = uuid.uuid4()
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 5
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SESSION_TYPE'] = 'sqlalchemy'
Session(app)
captcha = FlaskSessionCaptcha(app)

@app.route('/', methods=['POST','GET'])
def some_route():
    if request.method == "POST":
        if captcha.validate():
            return "success"
        else:
            return "fail"

    return render_template("form.html")

if __name__ == "__main__":
    app.debug = True
    logging.getLogger().setLevel("DEBUG")
    app.run(host="0.0.0.0", port=80)