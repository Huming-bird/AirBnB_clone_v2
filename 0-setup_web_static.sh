#!/usr/bin/env bash
# this script sets up my web servers for the deployment of web_static

sudo apt-get update
sudo apt-get install nginx

if [ ! -d /data ]; then sudo mkdir /data; fi
if [ ! -d /data/web_static ]; then sudo mkdir /data/web_static; fi
if [ ! -d /data/web_static/releases ]; then sudo mkdir /data/web_static/releases; fi
if [ ! -d /data/web_static/shared ]; then sudo mkdir /data/web_static/shared; fi
if [ ! -d '/data/web_static/releases/test' ]; then sudo mkdir /data/web_static/releases/test; fi
if [ ! -f /data/web_static/releases/test/index.html ]; then sudo touch /data/web_static/releases/test/index.html; fi
echo -e \<html\>\\n\\t\<head\>\<\/head\>\\n\\t\<body\>\\n\\t\\tHi I am Ahmed\\n\\t\<\/body\>\\n\<\/html\> > '/data/web_static/releases/test/index.html'
if [ -L /data/web_static/current ]; then sudo rm /data/web_static/current; else sudo ln -s '/data/web_static/releases/test' /data/web_static/current; fi
sudo chown -R ubuntu:ubuntu /data/
HBNB="server_name _;\n\tlocation \/hbnb_static\/ {\n\talias \/data\/web_static\/current;\n\t}"
sudo sed -i "s/server_name _;/$HBNB/" "/etc/nginx/sites-available/default"

sudo service nginx restart
