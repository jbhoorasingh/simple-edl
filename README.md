## Palo Alto Unofficial External Dynamic List Toolkit
This is side project to create and manage external dynamic list which can be reference in policies on Palo Alto Firewalls

This is written in Python using the Django framework.

### Why bother?
Why not? I have worked on various application leveraging Flask (flask-restx); the development of flask-restx has stalled/slowed, so I wanted to challenge myself to learn a new framework.

The choice was between Django and FastAPI - I choose Django because I'm not sure of the long-term maintenance of FastAPI with all the mini-me spawns showing up.

I decided to create this EDL toolkit because:
1) The poll/blog tutorial is just not my style. 
2) Speaking to some of my peers, I realized most want to leverage Palo Alto's EDL but are just using a text file on a webserver
3) Some think that MindMeld is a pain to maintain, and they don't want t pay for Autofocus

**TLDR**; Wanted to learn another Python web framework, Django > FastAPI, didn't want to create a poll/blog for my first Django project


## Quick Start: Development
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

### Environment File (.env)
```shell
# to be updated

```


## Acknowledgements
Dockerize Django Guide [TODO] - https://blog.logrocket.com/dockerizing-django-app/
