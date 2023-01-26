This is Django Rest API portfolio project

## Requirements

Django==4.1.5\
djangorestframework==3.14.0

### Additional libraries used:

django-filter==22.1\
django-versatileimagefield==2.2\
djangorestframework-simplejwt==5.2.2\
drf-flex-fields==1.0.0\
drf-spectacular==0.25.1\
python-magic-bin==0.4.14

## Set up
in terminal:

```bash
git clone https://github.com/peter-korkinov/celestial_bay_20_01_23.git
```

or simply download using the url:

[https://github.com/peter-korkinov/celestial_bay_20_01_23](https://github.com/peter-korkinov/celestial_bay_20_01_23)

&nbsp;

Then open the main project directory in terminal and run:

```bash
pip install -r requirements.txt
```
&nbsp;


To run the program in local server use the following command
```bash
python manage.py runserver
```
&nbsp;


Then go to [http://localhost:8000/](http://localhost:8000/) in your browser

To access the OpenAPI documentation open:
[http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

&nbsp;


### To migrate the database

```bash 
python manage.py makemigrations
python manage.py migrate
```
&nbsp;

### To use admin panel you need to create superuser using this command

``` bash
python manage.py createsuperuser
```
