[![Coverage Status](https://coveralls.io/repos/github/sudomakeinstall2/treez/badge.svg?branch=master)](https://coveralls.io/github/sudomakeinstall2/treez?branch=master)
# treez
Simple REST API implemented using `django` and `djangorestframwork`

#### installation
Make sure `docker` and `docker-compose` is installed.

##### build
```
docker-compose build
```
##### run
```
docker-compose up
```
After this step you can make requests to port 3000.
```
curl http://localhost:3000/inventories/
```
##### test
You can run the tests using:
```
docker-compose run web ./manage.py test
```
