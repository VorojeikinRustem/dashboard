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
The parameters(WEB_USER), (SERVER_NAME) are set correctly.
WEB_USER - $WEB_USER, SERVER_NAME - $SERVER_NAME
$WHITE"
    cd /home/$WEB_USER/venv/dashboard/
    mkdir tmp_dashboard
    cd tmp_dashboard/
    git clone https://github.com/Shoppr/DashboardsII.git
    cd ..
    cp -r /home/$WEB_USER/venv/dashboard/tmp_dashboard/DashboardsII/* /home/$WEB_USER/$HOME/
    rm -rf /home/$WEB_USER/venv/dashboard/DashboardsII/venv
    rm -rf /home/$WEB_USER/venv/dashboard/tmp_dashboard/*
elif [ -z "$1" ]&&[ -z "$2" ]
then
    echo -e "$RED 
Error. Parameters missing.$WHITE$EXAMPLE"
else
    echo -e "$RED
Error. Parameter №2(SERVER_NAME) missing.$WHITE$EXAMPLE"
fi
echo -en "$WHITE"
