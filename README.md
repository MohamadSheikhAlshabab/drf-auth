# Lab: Authentication & Production Server

- mkdir drf_auth
- cd drf_auth
- poetry init -n
- poetry add django djangorestframework  gunicorn whitenoise djangorestframework_simplejwt
- [//]: # (gunicorn to remove stuff from development side to production side)
- poetry shell
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver
- python manage.py makemigrations restaurant
- python manage.py migrate
- python manage.py runserver
- brew install httpie

---

## change ^ to ~

        # pyproject.toml
        python = "~3.8"

---

## in app views

        # app/views.py
        from django.shortcuts import render
        from rest_framework import generics
        from .models import Restaurant
        from .serializer import RestaurantSerializer
        from .permissions import IsAuthorOrReadOnly
        from rest_framework import permissions

        class RestaurantList(generics.ListCreateAPIView):
            queryset = Movie.objects.all()
            serializer_class = RestaurantSerializer

        class RestaurantDetails(generics.RetrieveUpdateDestroyAPIView):
            permission_classes = (IsAuthorOrReadOnly,)
            queryset = Movie.objects.all()
            serializer_class = RestaurantSerializer

---

## in app urls

        # app/urls.py
        from django.urls import path
        from .views import RestaurantList , RestaurantDetails

        urlpatterns = [
            path('rest',RestaurantList.as_view(), name='rest_list'),
            path('rest/<int:pk>',RestaurantDetails.as_view(), name='rest_details'),
        ]

---

## in app serializer

            # app/serializer.py
            from rest_framework import serializers
            from .models import Restaurant

            class RestaurantSerializer(serializers.ModelSerializer):
                class Meta:
                    fields = ('name_restaurant','count_waiters','stars','delivery','genre')
                    model = Restaurant

---

## in app models

            # app/models.py
            from django.db import models
            from django.contrib.auth import get_user_model

            class Restaurant(models.Model):
                name_restaurant = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
                count_waiters  = models.Count(models.CASCADE)
                stars = models.PositiveIntegerField()
                delivery = models.BooleanField()
                genre = models.CharField(max_length=64)

                def __str__(self):
                    return self.name_restaurant

---

## in app Dockerfile

            # app/Dockerfile
            FROM python:3.8
            ENV PYTHONDONTWRITEBYTECODE 1
            ENV PYTHONUNBUFFERED 1
            RUN mkdir /code
            WORKDIR /code
            COPY requirements.txt /code/
            RUN pip install -r requirements.txt
            COPY . /code/

---

## in app docker-compose.yml

[//]: <> (wsgi means web server gateway interface: describe how web server communicate with web application)

            # app/docker-compose.yml
            version: '3.8'
            services:
            web:
                build: .
                command: python manage.py runserver 0.0.0.0:8007
                # command: gunicorn management.wsgi:application --bind 0.0.0.0:8007 --workers 4
                volumes:
                - .:/code
                ports:
                - "8007:8007"

---

## in app admin

        # app/admin.py
        from django.contrib import admin
        from .models import Restaurant
        admin.site.register(Restaurant)

---

## in project urls

            # project/urls.py
            from django.contrib import admin
            from django.urls import path, include
            from rest_framework_simplejwt import views as jwt_views

            urlpatterns = [
                path('admin/', admin.site.urls),
                path('api/v1/rest/', include('restaurant.urls')),
                path('api-auth', include('rest_framework.urls')),
                path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
            ]

---

## in project settings

            # project/settings.py

            import os

            ALLOWED_HOSTS = ['0.0.0.0','127.0.0.1','localhost']

            INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'whitenoise.runserver_nostatic',
            'django.contrib.staticfiles',
            'rest_framework',                       # NEW
            'restaurant.apps.RestaurantConfig',     # NEW  
            ]

            MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'whitenoise.middleware.WhiteNoiseMiddleware',  # NEW
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            ]

            
            STATIC_DIR = os.path.join(BASE_DIR, 'static')
            STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
            STATIC_URL = '/static/'
            STATICFILES_DIRS = [
                STATIC_DIR,
            ]

            REST_FRAMEWORK = {
                'DEFAULT_PERMISSION_CLASSES': [
                    'rest_framework.permissions.IsAuthenticated',
                ],
                'DEFAULT_AUTHENTICATION_CLASSES':[
                    'rest_framework_simplejwt.authentication.JWTAuthentication',
                    'rest_framework.authentication.SessionAuthentication',
                    'rest_framework.authentication.BasicAuthentication',
                ]
            }

---

## add requirments.txt

- poetry export -f requirements.txt -o requirements.txt

---

## To access to API

- in one terminal: python manage.py runserver
- Create using POST
- in second terminal: http POST localhost:8007/api/token/ username='ggg' password='ggg123123'

        HTTP/1.1 200 OK
        Allow: POST, OPTIONS
        Content-Length: 438
        Content-Type: application/json
        Date: Wed, 30 Sep 2020 00:48:18 GMT
        Referrer-Policy: same-origin
        Server: WSGIServer/0.2 CPython/3.8.5
        Vary: Accept
        X-Content-Type-Options: nosniff
        X-Frame-Options: DENY

        {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjAxNDI3MTk4LCJqdGkiOiI0YWE1ZDNlMjRmOWI0ZmM5YjBlYTRmNGE2YWUyYTdlNiIsInVzZXJfaWQiOjN9.4sE2WPjGYdDr-SAHKxalDRO92pDTGQ9ri3q-PXlLQ4s",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwMTUxMzI5OCwianRpIjoiNjQzYTUyMTc2MzYwNGE2YTg5NWVmMDYxMjM1NmE3YjIiLCJ1c2VyX2lkIjozfQ.dsX06di86rn3nBFNugC6HS5IdCow1gSmwV0T-jJYaSc"
        }

- Read using GET
- in second terminal: http GET 0.0.0.0:8007/api/v1/rest/1 "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjAxNDI3MTk4LCJqdGkiOiI0YWE1ZDNlMjRmOWI0ZmM5YjBlYTRmNGE2YWUyYTdlNiIsInVzZXJfaWQiOjN9.4sE2WPjGYdDr-SAHKxalDRO92pDTGQ9ri3q-PXlLQ4s"

                HTTP/1.1 200 OK
                Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
                Content-Length: 64
                Content-Type: application/json
                Date: Wed, 30 Sep 2020 00:48:56 GMT
                Referrer-Policy: same-origin
                Server: WSGIServer/0.2 CPython/3.8.5
                Vary: Accept
                X-Content-Type-Options: nosniff
                X-Frame-Options: DENY

                {
                    "delivery": true,
                    "genre": "Arabic",
                    "name_restaurant": 2,
                    "stars": 5
                }

---

## in postman

- create collection: new collection
- put inside url the link of token:GET `http://127.0.0.1:8007/api/token/`
- and inside body: key:username  value:ggg
key:password value:ggg123123
- new collection: URL:GET `http://0.0.0.0:8007/api/v1/rest/`
- TOKEN: new Token
- to use refresh token: POST `http://0.0.0.0:8007/api/v1/refresh`
- Body: key: refresh value: put here tpken refresh

---

## issues

                (.venv) ➜  drf_auth docker-compose up --build
                ERROR:
                        Can't find a suitable configuration file in this directory or any
                        parent. Are you in the right directory?

                        Supported filenames: docker-compose.yml, docker-compose.yaml

                solution: 1- `sudo snap remove docker`
                - 2 - `sudo apt install docker.io docker-compose`