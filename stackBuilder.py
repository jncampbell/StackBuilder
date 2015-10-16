#!/usr/bin/env python
import subprocess, sys, datetime, shlex, os
from subprocess import Popen

class StackBuilder(object):


    def updateOS(self):
        self.summarizeOperation("Updating OS")
        print subprocess.call(shlex.split("sudo apt-get update"))


    def upgradeOS(self):
        self.summarizeOperation("Upgrading OS")
        print subprocess.call(shlex.split("sudo apt-get upgrade"))


    def installBuildDependencies(self):
        self.summarizeOperation("Installing Build Dependencies")
        self.installPackage("python-software-properties")
        self.installPackage("build-essential")


    def apache(self):
        self.summarizeOperation("Installing Apache Web Server")
        self.installPackage("apache2")


    def nginx(self):
        self.summarizeOperation("Installing Nginx Web Server")
        self.installPackage("nginx")


    def curl(self):
        self.summarizeOperation("Installing Curl")
        self.installPackage("curl")


    def php(self):
        #We put each package on a new line to improve readability
        self.summarizeOperation("Installing PHP")
        self.addRepository("ondrej/php5-5.6")
        self.installPackage("php5")
        self.installPackage("php5-fpm")
        self.installPackage("php5-common")
        self.installPackage("php5-dev")
        self.installPackage("php5-mcrypt")
        self.installPackage("php5-cli")
        self.installPackage("php5-curl")
        self.updateOS()
        print subprocess.call(shlex.split("sudo service nginx restart"))
        print subprocess.call(shlex.split("sudo service php5-fpm restart"))


    def mysql(self, password="root"):
        self.summarizeOperation("Installing MySQL")
        self.installPackage("php5-mysql")
        self.setMySQLPassword(password)
        self.installPackage("mysql-server")
        self.installPackage("mysql-client")


    def setMySQLPassword(self, password):
        command = shlex.split("sudo debconf-set-selections")
        inputPassword = Popen(command, stdin=subprocess.PIPE)
        inputPassword.communicate(input="mysql-server mysql-server/root_password password {0}".format(password))
        inputPasswordConfirm = Popen(command, stdin=subprocess.PIPE)
        inputPasswordConfirm.communicate(input="mysql-server mysql-server/root_password_again password {0}".format(password))


    def nodejs(self):
        self.summarizeOperation("Installing Nodejs")
        alias = open("/home/vagrant/.bash_aliases", "a")
        alias.write('alias node="nodejs"')
        alias.close()
        print subprocess.call(shlex.split("curl --silent --location https://deb.nodesource.com/setup_4.x | sudo bash "))
        self.installPackage("nodejs")
        self.installPackage("npm")


    def emacs(self):
        self.summarizeOperation("Installing Emacs")
        self.installPackage("emacs")


    def git(self):
        self.summarizeOperation("Installing Git")
        self.installPackage("git")


    def composer(self):
        self.summarizeOperation("Installing Composer")
        composer = Popen(shlex.split("curl -sS https://getcomposer.org/installer"), stdout=subprocess.PIPE)
        composerMove = Popen(shlex.split("sudo php -- --install-dir=/usr/local/bin --filename=composer"), stdin=composer.stdout)
        composerMove.communicate()[0]
        # print subprocess.call(shlex.split("curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer"))


    def installPackage(self, package):
        package = package.lower()
        command = shlex.split("sudo apt-get install -y " + package)
        try:
            print subprocess.check_call(command, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            if "unable to locate package" in e.output.lower():
                print "Can't identify package name. Check spelling of package name"
    

    def addRepository(self, repo):
        repo = repo.lower()
        command = shlex.split("sudo add-apt-repository -y ppa:"+repo)
        print subprocess.call(command)


    def summarizeOperation(self, operation):
        print "================ "+ operation +" ================"
        sys.stdout.flush()








