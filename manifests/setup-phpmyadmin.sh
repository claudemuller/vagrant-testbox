#!/usr/bin/env bash

echo "Creating vhost config for phpmyadmin..."
sudo cp /etc/apache2/sites-available/temp.local.conf /etc/apache2/sites-available/phpmyadmin.local.conf

echo "Creating symbolic link"
sudo ln -s /etc/apache2/sites-available/phpmyadmin.local.conf /etc/apache2/sites-enabled/phpmyadmin.local.conf

echo "Updating vhost config for phpmyadmin..."
sudo sed -i s,temp.local,phpmyadmin.local,g /etc/apache2/sites-available/phpmyadmin.local.conf
sudo sed -i s,/var/www/temp,/usr/share/phpmyadmin,g /etc/apache2/sites-available/phpmyadmin.local.conf

echo "So let's restart apache..."
sudo service apache2 restart
