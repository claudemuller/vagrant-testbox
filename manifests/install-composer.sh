#!/usr/bin/env bash

echo "Downloading and install composer..."
sudo curl -sS https://getcomposer.org/installer | php && sudo mv composer.phar /usr/bin/composer && sudo chmod 755 /usr/bin/composer
