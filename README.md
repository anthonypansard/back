# Backend for inc56

## Table of contents

* [What is inc56](#what-is-inc56)
* [What is in this repository](#what-is-in-this-repository)
* [Requirements](#requirements)
* [Folder structure](#folder-structure)
* [How to use](#how-to-use)

## What is inc56

The "inc56" project is a complete infrastructure including :

* *A connected multimedia object* that can be remotely controled
* *A mobile device* with an application to manage the client account / the connected object
* *A server infrastructure* to hold data and manage the interactions between the mobile device and the connected object

This project takes part of a first year course at the engineer school CentraleSupélec.

## What is in this repository

Here is the code for the server infrastructure. It is built using the python framework [Django](https://www.djangoproject.com/).

> It is still under construction and largely incomplete.

## Requirements

This project uses python `3.6` and Django `2.0`
The following python packages are also required :

* `lxml` (see [here](http://lxml.de/))
* `python-resize-image` (see [here](https://pypi.org/project/python-resize-image/))
* `Pillow` (see [here](https://pillow.readthedocs.io/en/5.1.x/))

## Folder structure

```
back/
    README.md                   -> This file
    alarm/                      -> Application handling the alarms
        admin.py                -> Customization for the default admin interface
        models.py               -> Models for the alarm application
        urls.py                 -> Url redirections for the alarm API
        views.py                -> Request processing and response
    back/                       -> Main folder of the project
        settings/               -> Django settings
            __init__.py         -> Modify this file to change the settings overide file
            base.py             -> Main setting file
            development.py      -> Settings overide for development environement
            testserver.py       -> Settings overide for the test server (not gited)
        db.sqlite3              -> Database file (not gited)
        urls.py                 -> Urls redirection for the applications
    BDD/                        -> Application hosting the main database
        management/
            commands/
                populate_bdd.py -> Automatically add fake data in the database
        admin.py                -> Customization for the default admin interface
        models.py               -> Main models
    media/                      -> Media files are stored here
        image/
        song/
        video/
    storage/                    -> Application hosting the file storage interface
        admin.py                -> Customization for the default admin interface
        models.py               -> Models for the storage application
        urls.py                 -> Url redirections for the storage API
        views.py                -> Request processing and response
    docs/                       -> Documentation
        index.md
```

## How to use

The full documentation, including all of the functionalities and the installation procedure can be found [here](docs/index.md).
