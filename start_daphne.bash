#!/bin/bash

NAME="bhossc-daphne"  # Name of the application
DJANGODIR=/home/ubuntu/webapp/bhossc  # Django project directory
DJANGOENVDIR=/home/ubuntu/webapp/bhossc/bhosscenv  # Django project env

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/ubuntu/webapp/bhosscenv/bin/activate
source /home/ubuntu/webapp/bhossc/.env
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start daphne
exec ${DJANGOENVDIR}/bin/daphne -u /home/ubuntu/webapp/bhosscenv/run/daphne.sock --access-log - --proxy-headers bhossc.asgi:application
