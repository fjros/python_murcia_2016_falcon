# -*- mode: ruby -*-
# vi: set ft=ruby :

# Requirements:
#  vagrant plugin install vagrant-hostsupdater
#  vagrant plugin install vagrant-vbguest

HOSTNAME = "falcon.meetup.dev"
IP = "192.168.0.2"

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
  end
end
