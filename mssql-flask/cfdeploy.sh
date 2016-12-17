#!/bin/sh

cf cups mssql -p '{"server":"hostname", "user":"username", "password":"password", "database":"dbname"}'

cf push mssql-flask --no-start

cf bind-service mssql-flask mssql

cf start mssql-flask
