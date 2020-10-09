#!/bin/bash

curl -i http://localhost:80/abc
curl -i -H "Content-Type: application/json" -X POST  http://localhost:80/abc  -d '{"abc": "10"}'

curl -i -X POST http://localhost:80/abc  -d '{"abc": "10"}'

curl -i http://localhost:80/multi/3
