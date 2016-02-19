# Python StackBuilder


## Description
StackBuilder is a python class that can install packages on Debian-based OSes. 
It's primarily used to setup development environments using Vagrant and VirtualBox.

Packages that usually take multiple commands to install are wrapped in a single method. 
For example, let's consider Nodejs. Currently, the lastest nodejs and npm builds are installed with the following:

`$ curl --silent --location https://deb.nodesource.com/setup_5.x | sudo -E bash -`
`$ sudo apt-get install nodejs`
`$ npm install -g npm@latest`

With Stackbuilder, this is performed by:

```python
builder = Stackbuilder()
builder.nodejs()
```

## Installation

* Import the libs directory into your project root. It contains the StackBuilder class and the \__init__.py file.

## Usage

* Create a bootstrap.py file in your root directory. This is where you will import and use the StackBuilder class. It should resemble something like this:

    ```python
    #!/usr/bin/env python
    
    from stackBuilder import StackBuilder
    builder = StackBuilder()
    builder.nginx()
    builder.vim()
    ```

* Add the following two lines to your Vagrantfile:

    ```ruby
    config.vm.provision :file, source: "libs/stackBuilder.py", destination: "/tmp/stackBuilder.py"
    config.vm.provision "shell", path: "bootstrap.py" 
    ```
    
* Run the `$ vagrant up` command from your project directory. 




