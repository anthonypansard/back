# Getting started

## Table of contents

* [Setup Django for developpement testing](#setup-django-for-developpement-testing)
* [Database](#database)
* [Authentification](#authentification)
  * [Authenticate](#authenticate)
  * [Create account](#create-account)
  * [Retrieve device list](#retrieve-device-list)
  * [Remove device](#remove-device)
  * [Retrieve connected object list](#retrieve-connected-object-list)
  * [Add connected object](#add-connected-object)
  * [Remove connected object](#remove-connected-object)
* [Alarm](#alarm)
  * [Retrieve alarm list](#retrieve-alarm-list)
  * [Add alarm](#add-alarm)
  * [Start and stop alarm](#start-and-stop-alarm)
  * [Delete alarm](#delete-alarm)
* [Comments](#comments)

## Setup Django for developpement testing

First make sure to install properly `python 3.6.4` and `Django 2.0`. The procedure varies depending on your operating system.<br>You also need to install `pip` and run `pip install -r requirements.txt`.

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

## Authentification

Authentification is needed for security reasons.
Each user needs to put it's credentials in a screen made for this purpose in the modile application before 
using it.

The server will check those credentials against the database and it will return a unique token linked both to the user and the device used if they are valid.

This token must be sent along any request made to the server afterward. It will be used to restrict the access to various ressources (like the alarms, the files, the connected objects owned...) only to the user's ones.

Thus, each request described below must be completed as follows:

```
~/?token=bd73be60-49dd-4518-95bd-4841259cd33a
```

For example, one must use this url to get the list of all the connected object owned:

```
localhost:8000/api/auth/beamy/?token=bd73be60-49dd-4518-95bd-4841259cd33a
```

>Note that this token is only an example and is not valid.

### Authenticate

Below, `imei` designate a unique code linked to the device used to open the user session

- **URL :**

  `GET ~/api/auth/?username=<username>&password=<password>&imei=<imei>`

- **URL Param :**

  `username`, required
  `password`, required
  `imei`, required

- **Data Param :**

  None

- **Success reponse :**

  Code : `200`

  Content :  `text/html`
  
  ```xml
  <?xml version="1.0"?>
  <set>
    <user>
      <username>solo</username>
      <firstname>han</firstname>
      <lastname>solo</lastname>
      <email>han.solo@sw.com</email>
      <token>bd73be60-49dd-4518-95bd-4841259cd33a</token>
    </user>
  </set>
  ```

- **Error response :**

  Code : `403`

  Returned if the credentials are invalid

  Code : `422`

  Returned if missing mandatory url parameters

- **Sample Call :**

  ```sh
  curl -X GET 'localhost:8000/api/auth/?username=solo&password=qwerty123456789&imei=1234'
  ```

### Create account

If the user account already exists, we just log in the user with the provided credentials

- **URL :**

  `POST ~/api/auth/`

- **URL Param :**

  None

- **Data Param :**

  ```xml
  <user>
      <username>solo</username>
      <password>qwerty123456789</password>
      <firstname>han</firstname>
      <lastname>solo</lastname>
      <email>han.solo@sw.com</email>
      <device_code>5555</device_code>
  </user>
  ```

- **Success reponse :**

  Code : `200`

  Content :  `text/html`

  ```xml
  <?xml version="1.0"?>
  <set>
      <user>
          <username>solo</username>
          <firstname>han</firstname>
          <lastname>solo</lastname>
          <email>han.solo@sw.com</email>
          <token>bd73be60-49dd-4518-95bd-4841259cd33a</token>
      </user>
  </set>
  ```

- **Error response :**

  None

- **Sample Call :**

  ```sh
  curl -X POST -d @new_user.xml 'http://localhost:8000/api/auth/'
  ```

### Retrieve device list

- **URL :**

  `GET ~/api/auth/device/int:id`

- **URL Param :**

  `id`, optional

- **Data Param :**

  None

- **Success reponse :**

  Code : `200`

  Content :  `text/html`
  
  ```xml
  <?xml version="1.0"?>
  <set>
      <device>
          <name>device</name>
          <id>4</id>
      </device>
  </set>
  ```

- **Error response :**

  None

- **Sample Call :**

  ```sh
  curl -X GET 'localhost:8000/api/device/?token=bd73be60-49dd-4518-95bd-4841259cd33a'
  ```

### Remove device

- **URL :**

  `DELETE ~/api/auth/device/int:id`

- **URL Param :**

  `id`, required

- **Data Param :**

  None

- **Success reponse :**

  Code : `200`

  Content :  `text/html`

  ```xml
  <?xml version="1.0"?>
  <set>
      <device>
          <name>device</name>
          <id>4</id>
      </device>
  </set>
  ```

- **Error response :**

  Code : `404`

  Return if no device is found

- **Sample Call :**

  ```sh
  curl -X DELETE 'localhost:8000/api/device/4/?token=bd73be60-49dd-4518-95bd-4841259cd33a'
  ```

### Retrieve connected object list

- **URL :**

  `GET ~/api/auth/beamy/int:id`

- **URL Param :**

  `id`, optional

- **Data Param :**

  None

- **Success reponse :**

  Code : `200`

  Content :  `text/html`

  ```xml
  <?xml version="1.0"?>
  <set>
      <beamy>
          <name>livingroom</name>
          <version>1.0</version>
          <id>2</id>
      </beamy>
      <beamy>
          <name>restroom</name>
          <version>1.0</version>
          <id>3</id>
      </beamy>
  </set>
  ```

- **Error response :**

  Code : `404`

  Returned if no device is found

- **Sample Call :**

  ```sh
  curl -X GET 'localhost:8000/api/beamy/?token=bd73be60-49dd-4518-95bd-4841259cd33a'
  ```

### Add connected object

Below, `pin` is a unique number written on the connected object.
It is used to prove one is the owner of the object (because one can read the `pin`)

*(Ok, this is not perfect. But it works for us)*

- **URL :**

  `POST ~/api/auth/beamy`

- **URL Param :**

  None

- **Data Param :**

  ```xml
  <beamy>
      <name>restroom</name>
      <pin>2222</pin>
  </beamy>
  ```

- **Success reponse :**

  Code : `200`

  Content :  `text/html`

  ```xml
  <?xml version="1.0"?>
  <set>
      <beamy>
          <name>livingroom</name>
          <version>1.0</version>
          <id>2</id>
      </beamy>
      <beamy>
          <name>restroom</name>
          <version>1.0</version>
          <id>3</id>
      </beamy>
  </set>
  ```

- **Error response :**

  Code : `422`

  Returned the data provided is incomplete

  Code : `404`

  Returned if the beamy matching `pin` can't be found

- **Sample Call :**

  ```sh
  curl -X POST -d @new_beamy.xml 'http://localhost:8000/api/auth/beamy/?token=bd73be60-49dd-4518-95bd-4841259cd33a'
  ```

### Remove connected object

- **URL :**

  `DELETE ~/api/auth/beamy/int:id`

- **URL Param :**

  `id`, required

- **Data Param :**

  None

- **Success reponse :**

  Code : `200`

  Content :  `text/html`

  ```xml
  <?xml version="1.0"?>
  <set>
      <beamy>
          <name>livingroom</name>
          <version>1.0</version>
          <id>2</id>
      </beamy>
  </set>
  ```

- **Error response :**

  Code : `404`

  Returned if the beamy matching `pin` can't be found

- **Sample Call :**

  ```sh
  curl -X DELETE 'http://localhost:8000/api/auth/beamy/3/?token=bd73be60-49dd-4518-95bd-4841259cd33a'
  ```

## Alarm

Alarm data is exchanged with the mobile device and the connected object using an API we designed.

All `xml` files with alarm data embedded have the same basis structure :

```xml
<alarm>
    <name>alarm_name</name>
    <!-- The alarm name -->
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

All wrong endpoints should return a `400` code.

### Retrieve alarm list

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
          <name>Get up!</name>
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
  curl -X GET 'http://localhost:8000/api/alarm/7/'
  ```

* **Notes**

  When a valid `id` parameter is used, the response xml contain only the alarm which internal id is `id`:

  ```xml
  <?xml version="1.0"?>
  <set>
  	<alarm>
          <name>Get up!</name>
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

### Add alarm

- **URL :**

  `POST ~/api/alarm/`

- **URL Param :**

  None

- **Data Param :**

  Content : `text/xml`

  ```xml
  <?xml version="1.0" ?> 
  <alarm>
      <name>Get up!</name>
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
      <name>Get up!</name>
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

  `running` can not set or unset by this request. You need to use a specific request. See [Start and stop alarm](#start-and-stop-alarm).

### Start and stop alarm

- **URL :**

  `GET ~/api/alarm/int:id/start`
  `GET ~/api/alarm/int:id/stop`

- **URL Param :**

  `id`, required

- **Data Param :**

  None

- **Success reponse :**

  Code : `200`

  Content :  `text/html`
  
  ```xml
  <?xml version="1.0" ?> 
  <alarm>
      <name>Get up!</name>
      <alarm_id>9</alarm_id>
      <beamy_id>2</beamy_id>
      <time>
          <day>wednesday</day>
          <hour>9</hour>
          <minute>56</minute>
      </time>
      <enabled>true</enabled>
      <running>true</running>
  </alarm>
  ```

- **Error response :**

  Code : `404`

  Returned if `id` does not correspond to any internal alarm id

- **Sample Call :**

  ```sh
  curl -H "Accept: text/xml" -H "Content-Type: text/xml" -X GET http://localhost:8000/api/alarm/7/start/
  ```

### Delete alarm

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