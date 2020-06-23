# Django 101

## What Django is?

Django is an extremely popular web-framework. It is very opiniated, synchronous (there is a work into async direction) and build around a relational database. 

Key element of Django is Django ORM - powerfull query builder with powerfull migration system. 

Django Admin - the autmatic admin interface that can be used to manage the data in the database. 

## Install Django

1. Create the virtual environment and activate the environment

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install Django 

   ```bash
   pip install django
   ```

3. Create a new django project

   ```bash
   django-admin startproject django101
   ```

   If `django-admin` is not available afrer the installation try to deactivate and activate your virtual environment.

4. CD to the newly created project

   ```bash
   cd django101
   ```

   This is how the project looks like now

   ```
   ├── django101
   │   ├── __init__.py
   │   ├── asgi.py
   │   ├── settings.py
   │   ├── urls.py
   │   └── wsgi.py
   └── manage.py
   ```

   ### Manage.py

   `django-admin` and `manage.py` are the same scripts. `django-admin` is executed from the system path, `manage.py` is added to the Django project directly. 

   These are equivalents:

   ```bash
   ./manage.py version
   python -m django version
   django-admin version
   ```

   To get the list of available commands run  `./manage.py` without arguments.

   ### Useful commands

   - **createsuperuser** - creates a super user for the Django
   - **makemigrations** - creates migration files if models changed
   - **migrate** - executes database migrations
   - **check** - runs static checks to validate the Django project
   - **runserver** - runs the Django development server

   

   The first command that we need to run is `./manage.py migrate`. It will create table to track migrations, manage users, admin application and user permissions. By default the app will use SQLite database, which is OK for the demo. On production most probably you will use Postgres or MySQL. The database connection settings can be changed in `settings.py`. 

## Create an app

```bash
cd django101
django-admin startapp customer
```

It creates a new application `customer` in our project. 

After we created an app, we need to add it to `INSTALLED_APPS` in `settings.py` which will enable the application.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django101.customer',
]
```



Now we can add models. 

## Models

Models are Python representations of the database records. 

Let's add a `customer` and customer's `stage` models.

```python
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    name = models.CharField(max_length=120)


class StageChoice(models.TextChoices):
    CLINIC = "CL", _("Clinic")
    PRECLINIC = "PC", _("Preclinic")


class Stage(models.Model):
    name = models.CharField(max_length=120, choices=StageChoice.choices)
```

Now we can create migrations for these models.

```bash
$ ./manage.py makemigrations                          
Migrations for 'customer':
  django101/customer/migrations/0001_initial.py
    - Create model Customer
    - Create model Stage
```

Migrations are created in `django101/customer/migrations/` folder. It's possible to review changes made by the migration by running `./manage.py sqlmigrate customer 0001`

```bash
$ ./manage.py sqlmigrate customer 0001 
BEGIN;
--
-- Create model Customer
--
CREATE TABLE "customer_customer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(120) NOT NULL);
--
-- Create model Stage
--
CREATE TABLE "customer_stage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(120) NOT NULL);
COMMIT;
```

Let's add a foreign key from the customer to the stage.

```python
class Customer(models.Model):
    name = models.CharField(max_length=120)
    stage = models.ForeignKey("customer.Stage", on_delete=models.CASCADE)
```

Let's apply the migration. The foreign key cannot be empty and we need to provide the defaul ID of the Stage that will be applied to existing Customer.

```bash

$ ./manage.py makemigrations customer
You are trying to add a non-nullable field 'stage' to customer without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option: 1
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
>>> 1
```

Let's review the SQL version of the migration

```bash
$ ./manage.py sqlmigrate customer 0002          
BEGIN;
--
-- Add field stage to customer
--
CREATE TABLE "new__customer_customer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "stage_id" integer NOT NULL REFERENCES "customer_stage" ("id") DEFERRABLE INITIALLY DEFERRED, "name" varchar(120) NOT NULL);
INSERT INTO "new__customer_customer" ("id", "name", "stage_id") SELECT "id", "name", 1 FROM "customer_customer";
DROP TABLE "customer_customer";
ALTER TABLE "new__customer_customer" RENAME TO "customer_customer";
CREATE INDEX "customer_customer_stage_id_c54183a8" ON "customer_customer" ("stage_id");
COMMIT;
```

## Django Admin

Django Admin allows to manage the data in the database with a nice UI which is easy to create and use.

To access the admin site we need to create a super user. 

```bash
./manage.py createsuperuser
```

Now we can run the server

```bash
./manage.py runserver
```

and access the admin site http://127.0.0.1:8000/admin/

