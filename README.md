# Email2Cloud

Aplicación que lee correos electrónicos y los sube a la nube

Esta pequeña aplicación consiste en un script de Python que hace lo siguiente:

1. Lee los correos de una cuenta de Gmail dentro de un intervalo de fechas
2. Copia cada uno de los correos al sistema de archivos local
3. Sube cada uno de estos archivos locales a una cuenta de Dropbox

## Cómo correr la aplicación

FYI: This app has been developed using Python version 3.12.

1. Install required dependencies

```
$ pip install -r requirements.txt
```

2. Enable Gmail API for your Google account and obtain a `client_secret.json` with OAuth 2.0 credentials:

   2.1 Go to Google Cloud Console:

   2.2 Create a new project (or select an existing one).

   2.3 Enable Gmail API:

- Navigate to APIs & Services > Library.
- Search for "Gmail API" and enable it.

  2.4 Create OAuth Credentials:

- Go to APIs & Services > Credentials.
- Click "Create Credentials" > "OAuth Client ID".
- Set Application type as Desktop app.
- Click Create, then Download JSON.

  2.5 Rename and place it in the project root:

- Save the downloaded file as `client_secret.json` in the project's root directory.

`client_secret.json` should look something like this:

```
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "YOUR_PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}
```

3. Run the script:

```
$ python app.py
```

After running the script for the first time, a `token.json` file will be generated, storing access and refresh tokens for future authentication.

## Detalles del Ambiente de Programación

A virtual environment has been created in this folder to avoid any library conflicts.

So, before you start working, remember to first start the virtual environment:

$ source bin/activate

You can deactivate the virtual environment by typing `deactivate` in your shell.
