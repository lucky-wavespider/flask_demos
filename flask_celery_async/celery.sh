#!/bin/bash

python ./send_email.py &
celery -A send_email.celery   worker


