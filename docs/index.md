# Getting started

## Table of contents

* [Setup Django for developpement testing](#setup-django-for-developpement-testing)
* [Database](#database)
* [Alarm](#alarm)
  * [Endpoints](#endpoints)
    * [Retrieve alarm list](#retrieve-alarm-list)
    * [Add alarm](#add-alarm)
    * [Delete alarm](#delete-alarm)
* [Comments](#comments)

## Setup Django for developpement testing

First make sure to install properly `python 3.6.4` and `Django 2.0`. The procedure varies depending on your operating system.<br>You also need to install `pip` and run `pip install-r requirements.txt`.

Clone/pull/download the repo.

Go to the project root directory.

Synchronize the databases

```sh
python manage.py migrate
```

Create a `superuser` account to acces the admin page

```sh
python manage.py createsuperuser # only before first run
```

Run the server

```sh
python manage.py runserver 0.0.0.0:8000
```

> NB : on linux systems, use `python3/pip3` instead of `python/pip`.

> NB : the server can't be deployed in production right away. Some security precautions are to be taken. Use these instruction only for testing purposes.

## Database

We have implemented the database using the default `sqlite3` server.

The current state of the tables is shown in the image below. The `User` table is different as we didn't implement it ourself. It is managed by default by Django. All other tables are defined in `/back/BDD/models.py`.

![Database architecture](images/database.png)

## Alarm

Alarm data is exchanged with the mobile device and the connected object using an API we designed.

All `xml` files with alarm data embedded have the same basis structure :

```xml
<alarm>
    <alarm_id>alarm_id</alarm_id>
    <!-- Only present in responses from the server -->
    <beamy_id>beamy_id</beamy_id>
    <!-- Should match an existing beamy id -->
    <time>
        <day>saturday, sunday</day>
        <!--
        Any subset of {monday, tuesday, wednesday, thursday, friday, saturday, sunday}
        Should be delimited by commas ","
        Spaces are truncated by the server
        -->
        <hour>10</hour>
        <!-- Should be an int in the range [0, 23] -->
        <minute>15</minute>
        <!-- Should be an int in the range [0, 59] -->
    </time>
    <enabled>true</enabled>
    <!-- Should be an element {true, false} -->
    <running>false</running>
    <!-- Only present in responses from the server -->
</alarm>
```

All values are treated as strings and no quotation marks are needed

### Endpoints

All wrong endpoints should return a `400` code.

#### Retrieve alarm list

* **URL :**


  `GET ~/api/alarm/int:id`

* **URL Param :**

  `id`, optional

* **Data Param :**

  None


* **Success reponse :**

  Code : `200`

  Content : `text/xml`

  ```xml
  <?xml version="1.0"?>
  <set>
      <alarm>
          <alarm_id>1</alarm_id>
          <beamy_id>1</beamy_id>
          <time>
              <day>monday, tuesday</day>
              <hour>8</hour>
              <minute>3</minute>
          </time>
          <enabled>true</enabled>
          <running>false</running>
      </alarm>
      <alarm>
      ...
      </alarm>
  </set>
  ```

* **Error response :**

  Code : `404`

  Returned if `id` does not correspond to any internal alarm id

* **Sample Call :**

  ```sh
  curl -H "Accept: text/xml" -H "Content-Type: text/xml" -X GET http://localhost:8000/api/alarm/7/
  ```

* **Notes**

  When a valid `id` parameter is used, the response xml contain only the alarm which internal id is `id`:

  ```xml
  <?xml version="1.0"?>
  <set>
  	<alarm>
          <alarm_id>id</alarm_id>
          <beamy_id>1</beamy_id>
          <time>
              <day>monday, tuesday</day>
              <hour>8</hour>
              <minute>3</minute>
          </time>
          <enabled>true</enabled>
          <running>false</running>
      </alarm>
  </set>
  ```


#### Add alarm

- **URL :**

  `POST ~/api/alarm/`

- **URL Param :**

  None

- **Data Param :**

  Content : `text/xml`

  ```xml
  <?xml version="1.0" ?> 
  <alarm>
      <beamy_id>2</beamy_id>
      <time>
          <day>wednesday</day>
          <hour>9</hour>
          <minute>56</minute>
      </time>
      <enabled>true</enabled>
  </alarm>
  ```


- **Success reponse :**

  Code : `200`

  Content :  `text/html`
  
  ```xml
  <?xml version="1.0" ?> 
  <alarm>
      <alarm_id>9</alarm_id>
      <beamy_id>2</beamy_id>
      <time>
          <day>wednesday</day>
          <hour>9</hour>
          <minute>56</minute>
      </time>
      <enabled>true</enabled>
      <running>false</running>
  </alarm>
  ```

- **Error response :**

  Code : `422`

  Returned if the `xml` data is invalid. See the required structure [here](#alarm).

  A message explaning the error comes along.

- **Sample Call :**

  ```sh
  curl -X POST -d @new_alarm.xml http://localhost:8000/api/alarm/
  ```

- **Note :**

  `running` can not set or unset by this request. You need to use a specific request. See [Stop alarm](#stop-alarm) and [Start alarm](#start-alarm).


#### Delete alarm

- **URL :**

  `DELETE ~/api/alarm/int:id`

- **URL Param :**

  `id`, required

- **Data Param :**

  None


- **Success reponse :**

  Code : `200`

  Content :  "hello"

- **Error response :**

  Code : `404`

  Returned if `id` does not correspond to any internal alarm id

- **Sample Call :**

  ```sh
  curl -X DELETE http://localhost:8000/api/alarm/5/
  ```

## Comments

Timezones are not yet well managed. We need to make sure each alarm rings at the right time in the right timezone.
For example, we live in `Europe/Paris` but Django default timezone is `UTC`.