<p align="center">
  <img src="docs/images/app_icon.png" width="200">
</p>
<h1 align="center"> DotA Notifier API Server</h1>

---

- [What is Dota Notifier API Server?](#what-is-dota-notifier-api-server)
- [Features](#features)
- [Usage and Installation](#usage-and-installation)

---


## What is DotA Notifier API Server?

The API Server behinds the DotA Notifier Mobile app https://github.com/noitq/dota_notifier_moible_app

DotA Notifier is an app allows users following DotA2 Pro Players. 

## Features

- [x] Auth APIs (login, signup, refersh token)
- [x] Subscribe/Unsubscribe a player API
- [x] Implement push notification using Firebase Cloud Messaging
- [x] Background worker for pulling new live matches using OpenDota Api
- [ ] Top followed Pro Players API
- [ ] Current live match on DotaTV API

## Usage and Installation

### Requirement
- Postgres Database for store user, channel, subscription info
- Google Firebase Account for push notification.

1. Clone this repository
```
$ git clone git@github.com:noitq/dota_notifier_server.git
```
2. Install the dependencies
```
$ pip install -r requirements.txt
```
3. set Environtment variables

Assume you are using linux system, we use the ```export``` command for setting ENV variable, if you are using Windows, please use equivalent command.

- Your app secret key (a strings you wish, such as 'absdfasdfasdf')
```
$ export SECRET_KEY = 'absdfasdfasdf'
```
- Postgres database uri such as 'postgres://mycduaaqgpcsjz:f0a56a53b4b450806@ec2-54-246-89-234.eu-west-1.compute.amazonaws.com:5432/abcd'
```
$ export SQLALCHEMY_DATABASE_URI = 'postgres://mycduaaqgpcsjz:f0a56a53b4b450806@ec2-54-246-89-234.eu-west-1.compute.amazonaws.com:5432/abcd'
```
- Firebase config
```
$ export FIREBASE_CONFIG = '{ your firebase config obtained from firebase console}'
```

4. Run server
```
$ flask run
```
Now your api server are running on local host.
