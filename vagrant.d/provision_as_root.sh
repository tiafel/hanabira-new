#!/usr/bin/env bash

DBNAME=hanadb
DBUSER=hana
DBPASSWD=some_password

echo -e "\n--- Install && configure python, MySQL, etc. ---\n"
cd /vagrant/

# locale
sed -i 's/# ru_RU\.UTF-8 UTF-8/ru_RU\.UTF-8 UTF-8/' /etc/locale.gen
locale-gen

if which apt-get > /dev/null; then
  # install some debian packages
  echo "mysql-server mysql-server/root_password password $DBPASSWD" | debconf-set-selections
  echo "mysql-server mysql-server/root_password_again password $DBPASSWD" | debconf-set-selections
  apt-get update
  apt-get -y install $(cat vagrant.d/apt.list | tr '\n' ' ')
elif which yum > /dev/null; then
  # install some centos packages
  yum -y update
  yum -y install $(cat vagrant.d/yum.list | tr '\n' ' ')
fi

echo -e "\n--- Setting up our MySQL user and db ---\n"
mysql -uroot -p$DBPASSWD -e "DROP DATABASE IF EXISTS $DBNAME"
mysql -uroot -p$DBPASSWD -e "CREATE DATABASE $DBNAME"
mysql -uroot -p$DBPASSWD -e "grant all privileges on $DBNAME.* to '$DBUSER'@'localhost' identified by '$DBPASSWD'"
mysql -u$DBUSER -p$DBPASSWD $DBNAME < hanabira.sql

echo -e "\n--- Install service ---\n"
cp vagrant.d/hana.sh /usr/local/bin/hana.sh
cp vagrant.d/hana.service /etc/systemd/system/hana.service
systemctl enable hana.service
