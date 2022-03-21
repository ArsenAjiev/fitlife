
# fitlife

### Create directory and .gitignore file
```shell
### Create weather_app directory
     mkdir fitlife
     
     cd fitlife/

### Venv
   
```shell
# Create environment
python3.8 -m venv --copies venv

# Activate
source venv/bin/activate

# Make sure to use venv/bin/pip3.8 
which pip3.8

```


### Install packages
```shell
pip install Django

pip install psycopg2-binary

pip install gunicorn

```


### Create Django project in app directory


```shell
django-admin startproject app

```
     cd app/

```shell
python manage.py startapp store
```

### Create and install requirements.txt in app directory.

      
```shell
pip freeze > requirements.txt

pip install -r requirements.txt
```
###Run db migrations

```shell
python manage.py makemigrations
python manage.py migrate
```




### How to access environment variable values
      
```shell

(venv) my_pc....../fitlife$ python
Python 3.8.10 (default, Nov 26 2021, 20:14:08) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> print(os.environ['SECRET_KEY'])
django-insecure-i5dfie@d1m*%-$rlk^%d@!=tghm)qxt1hcck9q^zn0aa=+_y10

    Or you can see a list of all the environment variables using:
>>> os.environ


```

# Docker


```shell
# clear ALL data !!! 
docker system prune -a
docker volume prune

```
```shell
# show information 
docker ps -a
docker images
docker volume ls

```

### Run all at once

```shell
docker-compose up -d --build --force-recreate
```

```shell
docker-compose exec app python manage.py createsuperuser
```

### Create some products
```shell
python manage.py create

```

