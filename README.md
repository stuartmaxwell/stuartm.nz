# stuartm.nz

The code for my stuartm.nz website.

## Requirements

- Django
- Postgres
- Whitenoise
- Gunicorn

## Installation

1. t.b.d.

## Usage

- Standard Django app

## Configuration

Rename `env.template` to `.env` and configure the following settings:

| Env Name            | Env Value                                                                                          |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| SECRET_KEY          | The Django secret key to add to the `settings.py` file.                                            |
| DEBUG               | Ensure this is set to `False` in production.                                                       |
| ALLOWED_HOSTS       | List of allowed hosts, e.g. `example.com,www.example.com`.                                         |
| EMAIL_HOST          | Name or IP address of the SMTP server.                                                             |
| EMAIL_PORT          | The port of the SMTP server.                                                                       |
| EMAIL_HOST_USER     | The username to authenticate with the SMTP server.                                                 |
| EMAIL_HOST_PASSWORD | The password for the SMTP server username.                                                         |
| EMAIL_USE_TLS       | Either `True` or `False` to use TLS.                                                               |
| DEFAULT_FROM_EMAIL  | The email address to send emails from .                                                            |
| DB_ENGINE           | The database engine to use.                                                                        |
| DB_NAME             | The database name to connect to. If using SQLite, this will be the filename without the extension. |
| DB_HOST             | Name or IP address of the database server.                                                         |
| DB_PORT             | The port of the database server.                                                                   |
| DB_USER             | The username to authenticate with the database server.                                             |
| DB_PASSWORD         | The password for the database server username.                                                     |
| WHITENOISE_STATIC   | Boolean value that turns on Whitenoise for serving static content.                                 |
| ADMIN_URL           | The path to the Admin site so it can be hidden from easily being guessed.                          |
