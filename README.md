# Error Reporting API
This is the final project of the Codenation Aceleradev Python - Stone course. The project goal was to develop an API for centralizing the application errors logs.

This REST API was built on top of [Django Rest Framework](https://www.django-rest-framework.org/).

## Prerequisites
This project was developed using Python 3.6.9, so it's recommended to install the same version because it wasn't tested in any other version. I suggest using [Virtualenv tool](https://virtualenv.pypa.io/en/latest/) for this purpose.

## Installation
- Clone this repo or download the files
- Navigate to the folder you cloned/download the files and execute:
```
pip install -r requirements.txt
```
- Run the migrations:
```
python manage.py migrate
```
- Create a superuser:
```
python manage.py createsuperuser
```

## Usage
First, run the django server:
```
python manage.py runserver
```
Since the endpoints are protected by Token Based Authentication, you will have make the following request to get a token:
```
Method: POST
Endpoint: /api/token
Body:
{
    "username": "<your-username>",
    "password": "<your-password>"
}
```

The JWT authentication was configured using the [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) and it's using the default expiration time for the Access Token, which is 5 minutes (and 1 day for the Refresh Token). If your Access Token expire, you have to refresh it doing the following request:
```
Method: POST
Endpoint: /api/token/refresh
Body:
{
    "refresh": "<your-refresh-token>"
}
```

Once you have the Access Token, you can use it in the other endpoints, for example, to list the Auth Users:
```
Method: GET
Endpoint: /api/users
Headers:
{
    "Authorization": "Bearer <your-access-token>"
}
```

The features available are:
- CRUD of Auth Users through the endpoint `/api/users`
- List/Create/Delete Events (error logs) through the endpoint `/api/events`
- Filter the results of the listing endpoints

For more details about the API usage, please read the [documentation](http://error-reporting-api.herokuapp.com/)

## API Reference
The API was documented using Swagger. There are two formats:
- [Swagger UI](https://error-reporting-api.herokuapp.com/) (you can test the API here)
- [ReDoc](https://error-reporting-api.herokuapp.com/redoc)
