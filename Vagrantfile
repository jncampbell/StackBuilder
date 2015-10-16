# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

    config.vm.box = "ubuntu/trusty64"

    config.vm.network "forwarded_port", guest:80, host:8080
    config.vm.network "private_network", ip: "192.168.33.10"

    config.vm.synced_folder "~/desktop/python-vagrant-wrapper", "/home/vagrant/python-vagrant-wrapper"

    config.vm.provision :file, source: "stackBuilder.py", destination: "/tmp/stackBuilder.py"
    config.vm.provision "shell", path: "bootstrap.py" 

end