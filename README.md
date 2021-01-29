# dad-jokes
Django web-app to demo some refactoring stuff

virtualenv -p python3 venv

pip install django
pip install requests

Had to install psycopg2 using:
https://stackoverflow.com/questions/26288042/error-installing-psycopg2-library-not-found-for-lssl
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip --no-cache install psycopg2