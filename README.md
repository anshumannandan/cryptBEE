<h1 align="center">cryptBEE</h1>

cryptBEE is a dummy trading crypto app made using Flutter for the frontend and Django for the backend. This repository contains the code for the backend part of the app. The frontend repository can be found [here](https://github.com/vaidic-dodwani/CryptbeeApp).


<h2 align="center">Key Features</h2>

CryptBEE offers essential features for cryptocurrency enthusiasts:

- Email (SMTP) for Signup/Signin.
- Two-Factor Authentication (2FA) with Enable/Disable through Phone Number utilizing Twilio.
- JWT Authentication with Refresh and Access tokens.
- Real-time WebSockets for updates.
- Fetching real time cryptocurrency data through WebScrapping & 3rd party endpoints.
- WebScrapping real time crypto NEWS.
- Buy, Sell, Transaction History.
- Dynamic Profit/Loss Calculator.
- Celery and Celerybeat for background tasking such as Sending Emails, SMS, Updating Coins information and NEWS in database.
- Deployment on AWS EC2 instance.
- Dockerized all the services (Backend, Celery, Celerybeat, Redis, PostgreSQL and Websocket).


<h2 align="center">PREVIEW</h2>

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


<h2 align="center">Running CryptBEE with Docker Compose</h2>

Follow these steps to set up and run CryptBEE using Docker Compose:

**Prerequisites:**

- Make sure you have Docker and Docker Compose installed on your machine. If not, you can [install them here](https://docs.docker.com/compose/install/).

**1. Clone the Repository:**

Clone the CryptBEE repository to your local machine using the following command:

```bash
git clone https://github.com/anshumannandan/cryptBEE
```

**2. Navigate to the project directory:**

```bash
cd cryptBEE
```

**3. Configure the Environment Variables:**

Edit the docker.env file located in the project's root directory to customize the environment variables to your specific requirements.

**4. Start the Containers:**

Build and start the Docker containers using the following command:

```bash
docker-compose up --build
```

This command will pull necessary images, build all the services, and start the containers.

**5. Access the CryptBEE Web:**

Once the containers are up and running, you can access the CryptBEE application in your web browser using the following URLs:

- **Backend:** [http://localhost:8000](http://localhost:8000)
- **WebSocket:** [ws://localhost:8001](ws://localhost:8001)

**Default Admin Credentials:**

Use the following credentials to access the admin panel:

- **Username:** admin@cryptbee.com
- **Password:** cryptbee

**Troubleshooting:**

./entrypoint.sh not found

- Open the `entrypoint.sh` file in a text editor.
- Change the line ending sequence to LF (Line Feed). You can usually do this by configuring your text editor to save the file with LF line endings.
- Save the changes to the `entrypoint.sh` file.
- Rebuild the containers using the `docker-compose up --build` command.

./entrypoint.sh: permission denied

- Grant execute permissions to the `entrypoint.sh` file using the following command:

```bash
sudo chmod +x entrypoint.sh
```

<h2 align="center">Setting Up CryptBEE on a Local Server</h2>

Follow these steps to set up CryptBEE on your local server:

**Prerequisites:**

1. **Python:** Make sure you have Python installed on your machine. If not, you can [install it here](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/).

2. **PostgreSQL:** Make sure you have PostgreSQL installed on your machine. If not, you can [install it here](https://www.postgresql.org/download/).

3. **Redis:** Make sure you have Redis installed on your machine. If not, you can [install it here](https://redis.io/download).

**Getting Started:**

**1. Clone the Repository:**

Clone the CryptBEE repository to your local machine using the following command:

```bash
git clone https://github.com/anshumannandan/cryptBEE
```

**2. Navigate to the project directory:**

```bash
cd cryptBEE
```

**3. Create and Activate a Virtual Environment:**

```bash
pip install virtualenv
virtualenv venv
venv/scripts/activate  # On Windows
source venv/bin/activate  # On Linux and macOS
```

**4. Install the Dependencies:**

```bash
pip install -r requirements.txt
```

**5. Configure the Environment Variables:**

Create a .env file in the cryptBEE/cryptBEE directory and add the following environment variables to it:

```env
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

**6. Create the Database:**

Create a PostgreSQL database and connect to it by entering credentials in .env file, once connected run the migrate command:

```bash
python manage.py migrate
```

**7. Create a Superuser:**

**You can create a superuser account executing the following commands:**

```bash
python manage.py createsuperuer
```

A prompt will appear asking for email followed by password.

**Alternatively, you can create a superuser by using the following custom command:**

```bash
python manage.py add_superuser --email <email> --password <password>
```

**8. Run the Backend Server:**

```bash
python manage.py runserver
```

**Access the endpoints in your web browaer:** [http://localhost:8000](http://localhost:8000)

**Access the Django Admin Panel, go to:** [http://localhost:8000/admin](http://localhost:8000/admin)

Use the superuser credentials to login.

**9. Run the Websocket Server:**

In a separate terminal with the virtual environment activated:

```bash
python websocket.py
```

You can connect to the websocket from your shell using this command:

```bash
python -m websockets ws://localhost:8001/
```

**10. Run Celery Worker:**

In a separate terminal with the virtual environment activated:

```bash
celery -A cryptBEE worker --pool=solo -l info
```

**11. Run Celery Beat:**

In a separate terminal with the virtual environment activated:

```bash
celery -A cryptBEE beat -l info
```

These steps will get you up and running with the CryptBEE backend on your local machine.


<div align="center">
  <h2>Frontend Contributor</h2>
  <h4><a href="https://github.com/vaidic-dodwani">VAIDIC DODWANI</a></h4>
</div>
