#!/bin/bash

curl -i http://localhost:80/abc
curl -i -H "Content-Type: application/json" -X POST  http://localhost:80/abc  -d '{"abc": "10"}'

curl -i -X POST http://localhost:80/abc  -d '{"abc": "10"}'

curl -i http://localhost:80/multi/3


curl -i http://localhost:80/todo/api/v1.0/tasks
curl -i http://localhost:80/todo/api/v1.0/tasks/2
curl -i http://localhost:80/todo/api/v1.0/tasks/112


curl -i -H "Content-Type: application/json" -X POST http://localhost:80/todo/api/v1.0/tasks -d '{"title": "test", "description": "just for test"}'


curl -i -H "Content-Type: application/json" -X PUT http://localhost:80/todo/api/v1.0/tasks/3 -d '{"title": "test2", "description": "just for test2", "done": true }'


curl -i -X DELETE http://localhost:80/todo/api/v1.0/tasks/3 
