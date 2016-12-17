#!/bin/sh

cf push mysql-flask --no-start

cf bind-service mysql-flask mysql

cf start mysql-flask
