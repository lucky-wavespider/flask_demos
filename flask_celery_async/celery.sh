#!/bin/bash

#export MAIL_USERNAME="abcdef@gmail.com"
#export MAIL_PASSWORD="abcdef"
echo "Please setting MAIL_USERNAME and MAIL_PASSWORD env."

python ./send_email.py &
celery -A send_email.celery   worker


