#!/usr/bin/env bash
# sets up web servers for the deployment of web_static

echo getting update
apt-get update -y > /dev/null 2>&1

echo installing nginx
apt-get install nginx -y > /dev/null 2>&1

echo making test dir
mkdir -p "/data/web_static/releases/test"

echo making shared folder
mkdir -p "/data/web_static/shared/"

echo "Huming-bird landing Page" > "/data/web_static/releases/test/index.html"

target_directory="/data/web_static/releases/test"
link_directory="/data/web_static/current"

echo checking for linked file
if [ -e "$link_directory" ]; then
    rm -f "$link_directory"
fi

echo creating linked file
ln -sf "$target_directory" "$link_directory"

echo changing ownership
chown -R ubuntu:ubuntu /data/

echo appending to nginx file
sed -i '/server_name _;/a \ \tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default


echo restarting nginx
service nginx restart > /dev/null 2>&1
