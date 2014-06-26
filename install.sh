#!/bin/bash

# Install the Langstroth web application on the demo server.
# The demo server publishes Langstroth using Apache2 and the WSGI module.

# Configure the langstroth.conf file to publish static content.
# See: https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/modwsgi/#serving-files
#sudo vi /etc/apache2/sites-available/langstroth.conf
#sudo service apache2 restart

# Will need to initially copy the install.sh script out of the archive
# After, for the first time only, executing the following line outside of the script.

# Export the web app from the source code repo.
LANGSTROTH_DISTRIBUTION=~/langstroth

if [ ! -d "$LANGSTROTH_DISTRIBUTION" ]; then
	git archive --format=tar --prefix=langstroth/ --remote=git@code.vpac.org:ncr002-dataanalysis/ncr002-langstroth.git  master | tar -xf -
fi

# Backup the previous web app.
TODAY=`date +"%Y%m%d"`
sudo mv /usr/local/django/langstroth /usr/local/django/langstroth-$TODAY
sudo mv ~/langstroth /usr/local/django

# Keep Apache2 and langstroth.conf happy.
# 1. Logging destination
sudo mkdir -p /usr/local/django/langstroth/apache/logs

# 2. Create the static content location.
sudo mkdir -p /usr/local/django/langstroth/static

# 3. Populate the static content location.
sudo cp -R /usr/local/django/langstroth/langstroth/static/* /usr/local/django/langstroth/static
sudo cp -R /usr/local/django/langstroth/langstroth/data/* /usr/local/django/langstroth/static

# Obsolete: at one time the js needed a tweak.
# Kept only as a recored.
#cd /usr/local/django/langstroth/langstroth/static/js
#sudo vi allocations_pie.js
