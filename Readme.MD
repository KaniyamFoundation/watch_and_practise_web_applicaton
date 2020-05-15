# Clone The Repository
```shell
git clone 
```
## Enter into the working directory

```shell
cd ystream
```
## Postgres is needed for this project to run
```shell
sudo apt install postgresql postgresql-contrib
```

## Install the requirements
```shell
virtualenv -p python3 envstream
. envstream/bin/activate
pip intsall -r requirements.txt
```
### Note: if this fails, supporting library is missing, google the error msg to solve the issue

## Create database in postgres

```shell
psql postgres 
create database ystream;
```
then exit the psql shell

## Needed ENVS for this project to set the envsetup file by
```shell
export DB_HOST=127.0.0.1
export DB_NAME=ystream
export DB_USER=<your-username>
export DB_PASS=<your-db-password>
export APP_ENV=dev
export TIME_ZONE=UTC
export SERVER_URL=http://localhost:8000/
export DJANGO_SETTINGS_MODULE=ystream.local
export ALLOWED_HOSTS=localhost
export SHELL_BASE_URL=<your-base-directory-for-shell>
export GUEST_BASE_DIR=<your-guests-directory>
export FROM_EMAIL=your-<from-email-address>
export EMAIL_API_KEY=<your-email-api-key>
export EMAIL_API_SECRET=<your-api-secret>
```
### Note: change the envs according to your dbname, pass, directory paths

## Finally migrate and run the server
```shell
python manage.py migrate
python manage.py runserver
```

## Open this on your browser
http://127.0.0.1:8000
