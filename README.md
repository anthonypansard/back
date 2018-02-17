# INC56

## Getting started

### System Requirements

Python `3.6`

Django `2.0`

### Setup Django

Go to the `back` directory

```sh
$ cd back
```

Synchronize the databases

```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

Create a `superuser` account to acces the admin page

```sh
$ python manage.py createsuperuser
```

NB :
On linux, use `python3` instead of `python`