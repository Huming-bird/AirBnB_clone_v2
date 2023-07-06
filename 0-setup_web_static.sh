#!/usr/bin/env bash
# this script sets up my web servers for the deployment of web_static

sudo apt-get update
sudo apt-get install nginx

sudo mkdir /data
sudo mkdir /data/web_static
sudo mkdir /data/web_static/releases
sudo mkdir /data/web_static/shared
sudo mkdir /data/web_static/releases/test
sudo touch /data/web_static/releases/test/index.html
if [ -L /data/web_static/current ]; then sudo rm /data/web_static/current; else sudo ln -s /data/web_static/releases/test /data/web_static/current; fi
sudo chown -R ubuntu:ubuntu /data/
HBNB="server_name _;\n\tlocation \/hbnb_static\/ {\n\talias \/data\/web_static\/current;\n\t}"
sudo sed -i "s/server_name _;/$HBNB/" "/etc/nginx/sites-available/default"

sudo service nginx restart
