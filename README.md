# cryptBEE

cryptBEE is a dummy trading crypto app made using Flutter for the frontend and Django for the backend. This repository contains the code for the backend part of the app. The frontend repository can be found [here](https://github.com/vaidic-dodwani/CryptbeeApp).

## FEATURES

- Email (SMTP) for Signup/Signin.
- Twilio for Phone Number Verification using OTP.
- Two-Factor Authentication (Enable/Disable).
- JWT Authentication with complete integration of Refresh and Access tokens.
- WebSockets for updating with data on frontend.
- Fetching real time cryptocurrency data through WebScrapping & 3rd party endpoints.
- WebScrapping real time crypto NEWS.
- Buy, Sell, Transaction History.
- Dynamic Profit/Loss Calculator.
- Celery and Celerybeat for background tasking (Sending Emails, SMS, Updating Coins information and NEWS in database).
- Deployment on Azure Virtual Machine (Ubuntu 20.04).

## PREVIEW

<p align="center">
  <img src="https://i.imgur.com/1RbcPs7.gif" width="200" />  
</p>

<p align="center">
  <img src="https://i.imgur.com/eLGO8Rt.png" width="150" />
  <img src="https://i.imgur.com/ruBacC4.png" width="150" />
  <img src="https://i.imgur.com/3DO7yGB.png" width="150" />
  <img src="https://i.imgur.com/8h2D4r4.png" width="150" />
  <img src="https://i.imgur.com/16XdyB5.png" width="150" />
</p>

<p align="center">
  <img src="https://i.imgur.com/iYDbHY1.png" width="150" />
  <img src="https://i.imgur.com/WVzYnEQ.png" width="150" />
  <img src="https://i.imgur.com/FoY9DU6.png" width="150" />
  <img src="https://i.imgur.com/g5FQa1m.png" width="150" />
  <img src="https://i.imgur.com/Gs4qxBZ.png" width="150" />
</p>

## RUNNING THE SERVER


1. Clone the repository:

```CMD
git clone https://github.com/anshumannandan/cryptBEE
```
To run the server, you need to have Python installed on your machine. If you don't have it installed, you can follow the instructions [here](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/) to install it.

2. Install & Create a virtual environment:

```CMD
pip install virtualenv
virtualenv venv
```
3. Activate the virtual environment:
```CMD
venv/scripts/activate
```

4. Navigate to the project directory: 

```CMD
cd cryptBEE
```

5. Install the dependencies: 

```CMD
pip install -r requirements.txt
```

6. Setup .env file in cryptBEE/cryptBEE and navigate back to base directory cryptBEE/:
```
SECRET_KEY=
DEBUG=

DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_DEFAULT_CALLERID=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

CRYPTOCOMPARE_API_KEY=
```

7. Create a PostgreSQL database and connect it by entering credentials in .env file, once connected run the migrate command:
```CMD
python manage.py migrate
```

8. You can create a superuser executing the following commands:
```CMD
python manage.py createsuperuer
```
A prompt will appear asking for email followed by password. 

9. Run the backend server on localhost:

```CMD
python manage.py runserver
```

You can access the endpoints from your web browser following this url:
```url
http://127.0.0.1:8000
```

To access the django admin panel follow this link and login through superuser credentials:
```url
http://127.0.0.1:8000/admin/
```

10. Run websocket server on localhost (On a separate terminal with activated virtual environment):

```CMD
python websocket.py
```

You can connect to websocket from your shell using this command:
```CMD
python -m websockets ws://localhost:8001/
```

12. To run the celery worker, you need to have Redis installed on your machine. If you don't have it installed, you can download and install it from [here](https://github.com/tporadowski/redis/releases).

12. Run celery worker (On a separate terminal with activated virtual environment):

```CMD
celery -A cryptBEE.celery worker --pool=solo -l info
```

13. Run celerybeat (On a separate terminal with activated virtual environment):

```CMD
celery -A cryptBEE beat -l info
```

## FRONTEND CONTRIBUTOR

[Vaidic Dodwani](https://github.com/vaidic-dodwani) - Contributed to the frontend part of the app.
