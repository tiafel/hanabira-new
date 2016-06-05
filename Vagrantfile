# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "debian/jessie64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  config.vm.provider :virtualbox do |vb|
    vb.memory = 512
  end
  config.vm.provider :lxc do |lxc|
      lxc.customize 'cgroup.memory.limit_in_bytes', '512M'
  end

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision :shell, inline: <<-SHELL
    DBNAME=hanadb
    DBUSER=hana
    DBPASSWD=some_password

    echo -e "\n--- Install && configure python, MySQL, etc. ---\n"
    cd /vagrant/
    if which apt-get >/dev/null; then
      # install some debian packages
      echo "mysql-server mysql-server/root_password password $DBPASSWD" | debconf-set-selections
      echo "mysql-server mysql-server/root_password_again password $DBPASSWD" | debconf-set-selections
      apt-get update
      apt-get -y install $(cat apt.list | tr '\n' ' ')
    elif which yum >/dev/null; then
      # install some centos packages
      yum -y update
      yum -y install $(cat yum.list | tr '\n' ' ')
    fi

    echo -e "\n--- Setting up our MySQL user and db ---\n"
    mysql -uroot -p$DBPASSWD -e "CREATE DATABASE $DBNAME"
    mysql -uroot -p$DBPASSWD -e "grant all privileges on $DBNAME.* to '$DBUSER'@'localhost' identified by '$DBPASSWD'"

    echo -e "\n--- Configure hanabira environment ---\n"
    virtualenv --no-site-packages -p /usr/bin/python3.4 ~/venv_hanabira
    echo "source ~/venv_hanabira/bin/activate" >> .profile
    source ~/venv_hanabira/bin/activate
    pip install -r requirements.txt
  SHELL
end
