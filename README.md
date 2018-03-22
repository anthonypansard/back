# Backend for inc56

## Table of contents

* [What is inc56](#what-is-inc56)
* [What is in this repository ?](#what-is-in-this-repository)
* [Requirements](#requirements)
* [Folder structure](#folder-structure)
* [How to use ?](#how-to-use)

## What is inc56

The "inc56" project is a complete infrastructure including :

* *A connected multimedia object* that can be remotely controled
* *A mobile device* with an application to manage the client account / the connected object
* *A server infrastructure* to hold data and manage the interactions between the mobile device and the connected object

This project takes part of a first year course at the engineer school CentraleSupélec

## What is in this repository

Here is the code for the server infrastructure. It is built using the python framework [Django](https://www.djangoproject.com/).
It is still under construction and largely incomplete

## Requirements

This project uses python `3.6` and Django `2.0`
The python package `lxml` is also required

## Folder structure

```
back/
	README.md			-> This file
	api/			    -> Folder for the `api` application
		urls.py			-> Url redirections for the API
		views.py		-> Request processing and response
	back/				-> Main folder of the project
		settings.py		-> Settings for Django
		urls.py			-> Urls base for the applications
	BDD/				-> Folder for the `BDD` application
		admin.py		-> Customization for the default admin interface
		models.py		-> Database models
	docs/				-> Documentation
		index.md
```

## How to use

The full documentation, including all of the functionalities and the installation procedure can be found [here](docs/index.md).