# -*- mode: ruby -*-
# vi: set ft=ruby :

# Requirements:
#  vagrant plugin install vagrant-hostsupdater
#  vagrant plugin install vagrant-vbguest

HOSTNAME = "falcon.meetup.dev"
IP = "192.168.0.2"
$script = <<SCRIPT
sudo apt-get update
sudo apt-get -y install python3-pip python3-dev
sudo pip3 install -r /vagrant/requirements.txt
sudo pip3 install -r /vagrant/requirements-test.txt
SCRIPT

# Configuration version 2 - do not change
Vagrant.configure("2") do |config|
  config.vm.define HOSTNAME do |machine|
    machine.vm.box = "ubuntu/trusty64"
    machine.vm.hostname = HOSTNAME
    machine.vm.network :private_network, ip: IP
    
    machine.vm.provider "virtualbox" do |vbox|
      vbox.name = HOSTNAME
      vbox.memory = 512
      vbox.cpus = 1
    end

    machine.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"
    machine.vm.provision "shell", inline: $script
  end
end
