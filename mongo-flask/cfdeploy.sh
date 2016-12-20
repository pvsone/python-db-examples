#!/bin/sh

cf cups mongo -p '{"server":"<mongo-host>", "port":"27017", "database":"test"}'

cf push mongo-flask --no-start

cf bind-service mongo-flask mongo

cf start mongo-flask
