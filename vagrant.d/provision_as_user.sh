#!/usr/bin/env bash

echo -e "\n--- Configure hanabira environment ---\n"
cd /vagrant/
virtualenv --no-site-packages -p /usr/bin/python3 $HOME/venv_hanabira
echo "source $HOME/venv_hanabira/bin/activate" >> .profile
source $HOME/venv_hanabira/bin/activate
pip install -r requirements.txt
