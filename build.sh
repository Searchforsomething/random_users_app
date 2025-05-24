#!/bin/bash

if ! command -v python3 &> /dev/null
then
    echo "Python3 not found"
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

python -m manage.py makemigrations
python -m manage.py migrate

python -m gunicorn random_user_app.wsgi:application --bind 0.0.0.0:8000 &

cd ../frontend

npm install
npm start &

wait