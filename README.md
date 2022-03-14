
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
pip install Django==4.0.2

pip install psycopg2-binary==2.9.3

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




