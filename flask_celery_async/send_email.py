import uuid
import logging
from flask_redis import FlaskRedis

from flask_mail import Message
from flask_mail import Mail

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from celery import Celery
import os

app = Flask(__name__)
app.secret_key = 'abc'  # 设置表单交互密钥
app.debug = True

mail = Mail(app)

#export FLASKR_SETTINGS="./setting.cfg"
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'applesmtp.yeah.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') #mimivpn@yeah.net
app.config['MAIL_PASSWORD'] = os.environ.get('mimiVPN123!') # MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = 'mimivpn@yeah.net'




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    email_data = {
        'subject': 'Hello from Flask',
        'to': email,
        'body': 'This is a test email sent from a background Celery task.'
    }
    if request.form['submit'] == 'Send':
        # send right away
        print("===> %s \n" % (email_data))
        send_async_email.delay(email_data)
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[email_data], countdown=5)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


@celery.task
def send_async_email(email_data):
    print("----> Go \n")
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    print("----> Go \n")
    with app.app_context():
        mail.send(msg)
        print("Send Done \n")



if __name__ == "__main__":
    #task = my_background_task.delay(10, 20)
    logging.getLogger().setLevel("DEBUG")
    app.run(host="0.0.0.0", port=80)