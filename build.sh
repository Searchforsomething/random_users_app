#!/bin/bash

if pgrep -x postgres > /dev/null; then
    echo "PostgreSQL is up"
else
    echo "PostgreSQL is down!"
    exit 1
fi

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo ".env successfully loaded"
else
    echo ".env not found!"
    exit 1
fi

cp .env random_user_app/random_user_app

echo "Creating randomuserdb..."
createdb -U "$DB_USER" randomuserdb


if ! command -v python3 &> /dev/null
then
    echo "Python3 not found!"
    exit 1
fi

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "venv created in ./venv"
else
    echo "venv already exists"
fi

source venv/bin/activate

pip install --upgrade pip

cd random_user_app

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found!!"
    deactivate
    exit 1
fi

echo "venv setup complete"

python manage.py makemigrations
python manage.py makemigrations users
python manage.py migrate

python -m gunicorn random_user_app.wsgi:application --bind 0.0.0.0:8000 &

cd ../frontend

npm install
npm start &

wait