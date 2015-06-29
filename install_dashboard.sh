#!/bin/bash
HOME="venv/dashboard/DashboardsII"
LCYAN='\033[1;36m'
RED='\033[0;31m'
WHITE='\033[37m'
PROJECT='DashboardsII'
EXAMPLE= '
Please enter the options :
WEB_USER and SERVER_NAME
The format: . install_dashboard.sh WEB_USER SERVER_NAME
Example:
. install_dashboard.sh ubuntu 52.74.174.156'
if [ -n "$1" ]&&[ -n "$2" ]
then
    WEB_USER=$1
    SERVER_NAME=$2
    echo -e "$LCYAN
The parameters($WEB_USER), ($SERVER_NAME) are set correctly.
WEB_USER - $WEB_USER, SERVER_NAME - $SERVER_NAME
$WHITE"
    cd /home/$WEB_USER/
    mkdir venv
    cd venv/
    sudo apt-get install python-setuptools
    sudo easy_install virtualenv
    virtualenv dashboard
    cd dashboard/
    source bin/activate
    pip install Django
    pip install pymongo
    pip install Fabric
    if  [ -e "$PROJECT" ]
    then
        rm -rf /home/$WEB_USER/venv/dashboard/$PROJECT
    fi
    git clone https://github.com/Shoppr/DashboardsII.git
    rm -rf /home/$WEB_USER/venv/venv
    rm -rf /home/$WEB_USER/venv/dashboard/venv
    python -c "
from pymongo import MongoClient
client = MongoClient()
db = client.dashboard
col=db.presets
if not col.find_one({'name':'local'}):
    col.insert_one({'name': 'local', 'host': '127.0.0.1', 'port': '27017', 'login': '', 'password': '', 'role': 'readWrite'})
"
    cd /home/$WEB_USER/$HOME/
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    pip install uwsgi
    sudo apt-get install nginx
    rm -rf /home/$WEB_USER/venv/dashboard/DashboardsII/venv
    touch dashboard_nginx.conf
    echo "
    def application(env, start_response):
        start_response('200 OK', [('Content-Type','text/html')])
        #return [b'Hello World'] # python3
        return ['Hello World'] # python2
    " > test.py

    echo "
    upstream django {
        #server 127.0.0.1:8001;
        server unix:///home/$WEB_USER/$HOME/dashboard.sock;
    }
    server {
        listen 80;
        server_name $SERVER_NAME;
        charset utf-8;
        client_max_body_size 75M;
        root /home/$WEB_USER/$HOME;
        access_log /var/log/nginx/dashboard.access.log;
        error_log /var/log/nginx/dashboard.error.log;
     
      location /media {
        alias /home/$WEB_USER/$HOME/media;
        }
        location /static {
        alias /home/$WEB_USER/$HOME/static;
        }
        location / {
           uwsgi_pass django;
           include /home/$WEB_USER/$HOME/uwsgi_params;
        }
    }
    " > dashboard_nginx.conf
    rm /etc/nginx/sites-enabled/shoppr_backend_rest_api.nginx.conf
    rm /etc/nginx/sites-enabled/shoppr_backend_crawler.nginx.conf
    rm /etc/nginx/sites-enabled/shoppr_backend_user_content.nginx.conf
    sudo ln -s /home/$WEB_USER/$HOME/dashboard_nginx.conf /etc/nginx/sites-enabled/
    sudo /etc/init.d/nginx restart
    touch dashboard_uwsgi.ini
    echo "
#dashboard_uwsgi.ini
[uwsgi]
chdir           = /home/$WEB_USER/$HOME/
module          = dashboard.wsgi
home            = /home/$WEB_USER/venv/dashboard
master          = true
processes       = 10
socket          = /home/$WEB_USER/$HOME/dashboard.sock
chmod-socket    = 666
vacuum          = true
    " > dashboard_uwsgi.ini
    deactivate
    sudo pip install uwsgi
    sudo mkdir /etc/uwsgi
    sudo mkdir /etc/uwsgi/vassals
    sudo ln -s /home/$WEB_USER/$HOME/dashboard_uwsgi.ini /etc/uwsgi/vassals/
    sudo sed -i.bak "/By default this script does nothing./a sudo uwsgi --emperor /etc/uwsgi/vassals/ --uid $WEB_USER --gid www-data" /etc/rc.local
    sudo uwsgi --emperor /etc/uwsgi/vassals --uid $WEB_USER --gid www-data
    uwsgi --ini dashboard_uwsgi.conf
elif [ -z "$1" ]&&[ -z "$2" ]
then
    echo -e "$RED 
Error. Parameters missing.$WHITE$EXAMPLE"
else
    echo -e "$RED
Error. Parameter SERVER_NAME missing.$WHITE$EXAMPLE"
fi
echo -en "$WHITE"
