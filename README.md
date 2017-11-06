# to-do-list

## Install

Having a Python3 virtualenv set up, run

    (to-do-list) $ pip install -r requirements.txt

## Migrate database

    (to-do-list) $ python manage.py migrate

## Run server

    (to-do-list) $ python manage.py runserver

## Configure sites options

As the frontend of the aplication will be host in another domain,
you have to configure its address populating the `django.contrib.sites.Site`
table.

Copy the contents of the fixtures example file, add your sites information to the fixture
and run django's `loaddata` command.

    $ cp fixtures.example.json fixtures.json

    $ python manage.py loaddata fixtures.json

Make sure the primary key you use on the fixture is the same one set on the
'SITE_ID' attribute on your settings file.

`settings_dev.py`

    SITE_ID = 1

`settings_prod.py`

    SITE_ID = 2

