# INC56

## Getting started

### System Requirements

Python `3.6`
Django `2.0`

### Setup Django

Go to the `back` directory

```sh
cd back
```

Synchronize the databases

```sh
python manage.py makemigrations # only if changes were made after git pull
python manage.py migrate
```

Create a `superuser` account to acces the admin page

```sh
python manage.py createsuperuser # only before first run
```

Run the server

```sh
python manage.py runserver
```

NB :
On linux, use `python3` instead of `python`

## Comments

Timezones are not yet well managed. We need to make sure each alarm rings at the right time in the right timezone.
For example, we live in `Europe/Paris` but Django default timezone is `UTC`.