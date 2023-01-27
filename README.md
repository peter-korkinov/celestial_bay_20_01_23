#### OpenAPI documentation available

This is Django Rest API back-end project. Within it users can register a profile. Then they can create records of the galaxies they own containing data of the galaxy's properties and images of it. Users can also create posts with images and comment under them. It is set up by default for use with PostgreSQL.

It contains two apps - "my_auth" and "galaxies".

"my_auth" has a custom user model with email instead of username and uuid pk. It has funtionality for registering new users, authentication via JSON Web Token using the SimpleJWT library, changing password, updating and retrieving user info and logout.

"galaxies" has two main models - Galaxy and Post, five auxiliary ones - GalaxyImage, PostImage, Comment, Constellation and ConstellationImage. Their instances are available as read-only unless the user is authenticated as their owner.

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
If you encounter
```
ImportError('failed to find libmagic.  Check your installation')
```
you can try
```
pip uninstall python-magic
```
&nbsp;


Then go to [http://localhost:8000/](http://localhost:8000/) in your browser

To access the **OpenAPI** documentation open:
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
