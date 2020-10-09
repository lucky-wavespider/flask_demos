import uuid
import logging
from flask_redis import FlaskRedis

from flask_mail import Message
from flask_mail import Mail

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

from celery import Celery
import os


def app_cfg_init():
    # export FLASKR_SETTINGS="./setting.cfg"
    # app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    fk_app = Flask(__name__)
    fk_app.secret_key = 'abc'  # 设置表单交互密钥
    fk_app.debug = True
    return fk_app


def celery_cfg_init(app):
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    cy = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    cy.conf.update(app.config)
    return cy


def email_cfg_init(app):
    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.yeah.net'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = 'mimivpn@yeah.net'
    app.config['MAIL_ASCII_ATTACHMENTS'] = True
    app.config['MAIL_DEBUG'] = True

    #print("User: '%s', Pass: '%s' \n" % ( app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'] ))
    ml = Mail(app)
    return ml


app = app_cfg_init()
celery = celery_cfg_init(app)
mail = email_cfg_init(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email_addr = request.form['email']
    session['email'] = email_addr

    # send the email
    email_data = {
        'subject': 'Hello from Flask',
        'to': email_addr,
        'body': 'This is a test email sent from a background Celery task.'
    }

    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(email_data)
        flash('Sending email to {0}'.format(email_data))
    else:
        # send in one minute
        send_async_email.apply_async(args=[email_data], countdown=5)
        flash('An email will be sent to {0} in one minute'.format(email_data))

    return redirect(url_for('index'))


@celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']

    with app.app_context():
        print("User: '%s', Pass: '%s' \n" % (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
        mail.send(msg)

#Just for test email only.
def test_send_email():
    msg = Message("abc", sender=app.config['MAIL_DEFAULT_SENDER'], recipients=["mimivpn@yeah.net"])
    msg.body = "hello world !!!\n"

    with app.app_context():
        app.extensions['mail'].send(msg)


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")
    app.run(host="0.0.0.0", port=80)
