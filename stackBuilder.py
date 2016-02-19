#!/usr/bin/env python
import subprocess, sys, shlex
from subprocess import Popen


class StackBuilder(object):

    def __init__(self):
        self.update_os_packages()
        self.upgrade_os_packages()

    def update_os_packages(self):
        self.summarize_operation("Updating OS Packages")
        print subprocess.call(shlex.split("sudo apt-get update -y"))

    def upgrade_os_packages(self):
        self.summarize_operation("Upgrading OS Packages")
        print subprocess.call(shlex.split("sudo apt-get upgrade -y"))

    def install_package(self, package):
        package = package.lower()
        command = shlex.split("sudo apt-get install -y " + package)
        try:
            print subprocess.check_call(command, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            if "unable to locate package" in e.output.lower():
                print "Can't identify package name. Check spelling of package name"

    def add_repository(self, repo):
        repo = repo.lower()
        command = shlex.split("sudo add-apt-repository -y ppa:"+repo)
        print subprocess.call(command)

    def summarize_operation(self, operation):
        print "================ "+ operation +" ================"
        sys.stdout.flush()

    def python_software_properties(self):
        self.install_package("python-software-properties")

    def build_essential(self):
        self.install_package("build-essential")

    def apache(self):
        self.summarize_operation("Installing Apache Web Server")
        self.install_package("apache2")

    def nginx(self):
        self.summarize_operation("Installing Nginx Web Server")
        self.install_package("nginx")

    def curl(self):
        self.summarize_operation("Installing Curl")
        self.install_package("curl")

    def php(self):
        # We put each package on a new line to improve readability
        self.summarize_operation("Installing PHP")
        self.add_repository("ondrej/php5-5.6")
        self.install_package("php5")
        self.install_package("php5-fpm")
        self.install_package("php5-common")
        self.install_package("php5-dev")
        self.install_package("php5-mcrypt")
        self.install_package("php5-cli")
        self.install_package("php5-curl")
        self.update_os_packages()
        print subprocess.call(shlex.split("sudo service nginx restart"))
        print subprocess.call(shlex.split("sudo service php5-fpm restart"))

    def mysql(self, password="root"):
        self.summarize_operation("Installing MySQL")
        self.install_package("php5-mysql")
        self.set_mysql_password(password)
        self.install_package("mysql-server")
        self.install_package("mysql-client")

    def set_mysql_password(self, password):
        command = shlex.split("sudo debconf-set-selections")
        input_password = Popen(command, stdin=subprocess.PIPE)
        input_password.communicate(input="mysql-server mysql-server/root_password password {0}".format(password))
        input_password_confirm = Popen(command, stdin=subprocess.PIPE)
        input_password_confirm.communicate(input="mysql-server mysql-server/root_password_again password {0}".format(password))

    def nodejs(self):
        self.summarize_operation("Installing Nodejs")
        process = Popen(shlex.split("curl --silent --location https://deb.nodesource.com/setup_5.x"), stdout=subprocess.PIPE)
        process_stdout = Popen(shlex.split("sudo -E bash -"), stdin=process.stdout)
        process_stdout.communicate()[0]
        self.install_package("nodejs")
        self.npm_install_globally("npm@latest")

    def npm_install_globally(self, package):
        self.summarize_operation("Installing " + package)
        print subprocess.call(shlex.split("sudo npm install -g " + package))

    def npm_install(self, package):
        self.summarize_operation("Installing " + package)
        print subprocess.call(shlex.split("sudo npm install --save " + package))

    def emacs(self):
        self.summarize_operation("Installing Emacs")
        self.install_package("emacs")

    def vim(self):
        self.summarize_operation("Installing Vim")
        self.install_package("vim")

    def git(self):
        self.summarize_operation("Installing Git")
        self.install_package("git")

    def composer(self):
        self.summarize_operation("Installing Composer")
        composer = Popen(shlex.split("curl -sS https://getcomposer.org/installer"), stdout=subprocess.PIPE)
        composer_move = Popen(shlex.split("sudo php -- --install-dir=/usr/local/bin --filename=composer"), stdin=composer.stdout)
        composer_move.communicate()[0]









