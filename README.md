RUN A PROJECT
==============

1. Create a virtual env and activate the environment
2. Install all dependencies by `pip install -r requirements.txt`
3. Create **.env** file and add following data
    - SECRET_KEY
    - EMAIL_USE_TLS
    - DEFAULT_FROM_EMAIL
    - SERVER_EMAIL
    - EMAIL_HOST
    - EMAIL_PORT
    - EMAIL_HOST_USER
    - EMAIL_HOST_PASSWORD
    - EMAIL_BACKEND
    - DATABASE_ENGINE
    - DATABASE_NAME
    - DATABASE_USER
    - DATABASE_PASSWORD
    - STAGING_DATABASE_NAME
    - STAGING_DATABASE_USER
    - STAGING_DATABASE_PASSWORD
    - DATABASE_HOST
    - DATABASE_PORT
4. Configure whether to use dev server or production server by modifying in manage.py, project/wsgi.py and project/asgi.py as either **"project.settings.dev"** or **"project.settings.prod"**
5. run `python manage.py makemigrations`
6. run `python manage.py migrate`
7. run `python manage.py createsuperuser`
8. run `python manage.py runserver`