## Simple External Dynamic List Toolkit
This is side project to create and manage external dynamic list which can be reference in policies on Palo Alto and Checkpoint firewalls.

This is written in Python using the Django framework.

### Why bother?
Why not? I have worked on various application leveraging Flask (flask-restx); the development of flask-restx has stalled/slowed, so I wanted to challenge myself to learn a new framework.

The choice was between Django and FastAPI - I choose Django because I'm not sure of the long-term maintenance of FastAPI with all the mini-me spawns showing up.

I decided to create this EDL toolkit because:
1) The poll/blog tutorial is just not my style. 
2) Speaking to some of my peers, I realized most want to leverage Palo Alto's EDL but are just using a text file on a webserver
3) Some think that MindMeld is a pain to maintain, and they don't want t pay for Autofocus

**TLDR**; Wanted to learn another Python web framework, Django > FastAPI, didn't want to create a poll/blog for my first Django project

## Live Demo
Any data entered into the live demo will be deleted every 24 hours.

| Demo Site | Username | Password |
|----------|----------|----------|
| http://demo1.simpleedl.com/gui/ | demouser1 | bl3buS1tEnTEmEKT1n |

If you are thinking about trying this out - please consider using the Digital Ocean referral link below. You will get $200 credit for 60 days, and I will get $25 credit to help run this demo.

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=0fea2173d2fd&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

You can also support this project by buying me a coffee.

<a href="https://www.buymeacoffee.com/jermainebh1" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="60px" width="217px"></a>


## Quick Start
### Development (No Docker)
```shell
# Clone repo
git clone https://github.com/jbhoorasingh/simple-edl.git

# Set up python environment
python -m venv venv
source ./venv/bin/activate
pip install -r requirments.txt

# Migrate database - this will create a temp sqlite3 db
python manage.py makemigrations
python manage.py migrate

# create superuser
python manage.py createsuperuser

```



#### Environment File

##### .env

```shell
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=KeKeDoYouLoveMe_NoIDont
DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
DJANGO_TIME_ZONE=UTC
DJANGO_DB_ENGINE=django.db.backends.postgresql
DJANGO_DB_NAME=simple_edl
DJANGO_DB_USER=simple_edl
DJANGO_DB_PASSWORD=HelloW0rld2024YouShouldChangeThisPlzPlz
DJANGO_DB_HOST=db
DJANGO_DB_PORT=5432
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

##### .env.db

Separating out Database so we can easily decouple

```shell
POSTGRES_USER=r_networking_ping # Change if desired. Has to match SQL_USER in .env
POSTGRES_PASSWORD=ChangeMePlease # Please change! Has to match SQL_USER in .env
POSTGRES_DB=r_networking_pingn # Change if desired. Has to match SQL_USER in .env
```

### Development (Docker)

#### Docker Compose Up

```shell
docker-compose -f docker-compose.dev.yml up --build
```

#### Docker Compose Create Super User (Optional)

```shell
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```



## Acknowledgements
Dockerize Django Guide [TODO] - https://blog.logrocket.com/dockerizing-django-app/
