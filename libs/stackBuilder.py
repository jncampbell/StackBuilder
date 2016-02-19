#!/usr/bin/env python
import subprocess, sys, shlex
from subprocess import Popen


class StackBuilder(object):

    def __init__(self):
        """
        Perform initial update and upgrade operations for packages on the OS.

        Notes:
            Many package installations will fail without updates/upgrades to the OS packages.
        """
        self.update_os_packages()
        self.upgrade_os_packages()

    def update_os_packages(self):
        """
        Update packages installed on the OS
        """
        self.summarize_operation("Updating OS Packages")
        print subprocess.call(shlex.split("sudo apt-get update -y"))

    def upgrade_os_packages(self):
        """
        Upgrade packages install on the OS
        """
        self.summarize_operation("Upgrading OS Packages")
        print subprocess.call(shlex.split("sudo apt-get upgrade -y"))

    def install_package(self, package):
        """
        Install a package on the OS

        Args:
            package: the package to be installed

        Notes:
            The '-o Dpkg::Options::="--force-confold" --force-yes' option does not modify the current config file.
            The new version is installed with a .dpkg-dist suffix.
            See https://raphaelhertzog.com/2010/09/21/debian-conffile-configuration-file-managed-by-dpkg/ for more info

        Raises:
            CalledProcessError: if the package can't be found
        """
        package = package.lower()
        command = shlex.split('sudo DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" --force-yes -y install ' + package)
        try:
            print subprocess.check_call(command, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            if "unable to locate package" in e.output.lower():
                print "Can't identify package name. Check spelling of package name"

    def add_repository(self, repo):
        """
        Add a repository to the OS

        Args:
            repo: the repository to be added
        """
        repo = repo.lower()
        command = shlex.split("sudo add-apt-repository -y ppa:"+repo)
        print subprocess.call(command)

    def summarize_operation(self, operation):
        """
        Print to the console a description of the operation being performed

        Args:
            operation: the operation being performed
        """
        print "================ "+ operation +" ================"
        sys.stdout.flush()

    def python_software_properties(self):
        """
        Install the python-software-properties package
        """
        self.install_package("python-software-properties")

    def build_essential(self):
        """
        Install the build-essential package
        """
        self.install_package("build-essential")

    def apache(self):
        """
        Install the apache web server package
        """
        self.summarize_operation("Installing Apache Web Server")
        self.install_package("apache2")

    def nginx(self):
        """
        Install the nginx web server package
        """
        self.summarize_operation("Installing Nginx Web Server")
        self.install_package("nginx")

    def curl(self):
        """
        Install the curl package
        """
        self.summarize_operation("Installing Curl")
        self.install_package("curl")

    def php(self):
        """
        Install PHP 5.6

        Notes:
            We put each install_package command on its own line to improve readability
        """
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
        """
        Install mysql

        Args:
            password: the password to be set for mysql.

        Notes:
            Both the username and password default to "root"
        """
        self.summarize_operation("Installing MySQL")
        self.install_package("php5-mysql")
        self.set_mysql_password(password)
        self.install_package("mysql-server")
        self.install_package("mysql-client")

    def set_mysql_password(self, password):
        """
        Set the mysql password

        Args:
            password: the password to be set
        """
        command = shlex.split("sudo debconf-set-selections")
        input_password = Popen(command, stdin=subprocess.PIPE)
        input_password.communicate(input="mysql-server mysql-server/root_password password {0}".format(password))
        input_password_confirm = Popen(command, stdin=subprocess.PIPE)
        input_password_confirm.communicate(input="mysql-server mysql-server/root_password_again password {0}".format(password))

    def nodejs(self):
        """
        Install and then update NodeJS
        """
        self.summarize_operation("Installing Nodejs")
        process = Popen(shlex.split("s"), stdout=subprocess.PIPE)
        process_stdout = Popen(shlex.split("sudo -E bash -"), stdin=process.stdout)
        process_stdout.communicate()[0]
        self.install_package("nodejs")
        self.npm_install_globally("npm@latest")

    def npm_install_globally(self, package):
        """
        Install an npm package globally

        Args:
            package: the package to be installed
        """
        self.summarize_operation("Installing " + package)
        print subprocess.call(shlex.split("sudo npm install -g " + package))

    def npm_install(self, package):
        """
        Install an npm package locally

        Args:
            package: the package to be installed
        """
        self.summarize_operation("Installing " + package)
        print subprocess.call(shlex.split("sudo npm install --save " + package))

    def emacs(self):
        """
        Install Emacs
        """
        self.summarize_operation("Installing Emacs")
        self.install_package("emacs")

    def vim(self):
        """
        Install Vim
        """
        self.summarize_operation("Installing Vim")
        self.install_package("vim")

    def git(self):
        """
        Install Git
        """
        self.summarize_operation("Installing Git")
        self.install_package("git")

    def composer(self):
        """
        Install Composer

        Notes:
            PHP must be installed for the installation to be successful
        """
        self.summarize_operation("Installing Composer")
        composer = Popen(shlex.split("curl -sS https://getcomposer.org/installer"), stdout=subprocess.PIPE)
        composer_move = Popen(shlex.split("sudo php -- --install-dir=/usr/local/bin --filename=composer"), stdin=composer.stdout)
        composer_move.communicate()[0]









