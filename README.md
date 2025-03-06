# Email2Cloud

Aplicación que lee correos electrónicos y los sube a la nube

Esta pequeña aplicación consiste en un script de Python que hace lo siguiente:

1. Lee los correos de una cuenta de Gmail dentro de un intervalo de fechas
2. Copia cada uno de los correos al sistema de archivos local
3. Sube cada uno de estos archivos locales a una cuenta de Dropbox

## Cómo correr la aplicación

$ python app.py

## Detalles del Ambiente de Programación

A virtual environment has been created in this folder to avoid any library conflicts.

So, before you start working, remember to first start the virtual environment:

$ source bin/activate

You can deactivate the virtual environment by typing `deactivate` in your shell.
