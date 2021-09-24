# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "hashicorp/bionic64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

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

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
  
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
	export PROFILE=/home/vagrant/.profile
    export INSTALL_ROOT="/home/vagrant"
    cd ${INSTALL_ROOT}
	    sudo apt-get update
    # Install pyenv prerequisites
    export BUILD_LIBS="build-essential"
    export BUILD_LIBS="${BUILD_LIBS} libssl-dev"
    export BUILD_LIBS="${BUILD_LIBS} zlib1g-dev"
    export BUILD_LIBS="${BUILD_LIBS} libbz2-dev"
    export BUILD_LIBS="${BUILD_LIBS} libreadline-dev"
    export BUILD_LIBS="${BUILD_LIBS} libsqlite3-dev"
    export BUILD_LIBS="${BUILD_LIBS} wget"
    export BUILD_LIBS="${BUILD_LIBS} curl"
    export BUILD_LIBS="${BUILD_LIBS} llvm"
    export BUILD_LIBS="${BUILD_LIBS} libncursesw5-dev"
    export BUILD_LIBS="${BUILD_LIBS} xz-utils"
    export BUILD_LIBS="${BUILD_LIBS} tk-dev"
    export BUILD_LIBS="${BUILD_LIBS} libxml2-dev"
    export BUILD_LIBS="${BUILD_LIBS} libxmlsec1-dev"
    export BUILD_LIBS="${BUILD_LIBS} libffi-dev"
    export BUILD_LIBS="${BUILD_LIBS} liblzma-dev"
    sudo apt-get --yes install make ${BUILD_LIBS}
    # Prep pyenv env
    export VAGRANT_INSTALL=${INSTALL_ROOT}/.pyenv
    # Install pyenv
    git clone https://github.com/pyenv/pyenv.git ${VAGRANT_INSTALL}
    export PATH=${VAGRANT_INSTALL}/bin:${PATH}
    # Update ~/.profile
    echo "" >> ${PROFILE}
    echo "# set Vagrant env vars" >> ${PROFILE}
    echo "export VAGRANT_INSTALL=${VAGRANT_INSTALL}" >> ${PROFILE}
    echo "export PATH=${VAGRANT_INSTALL}/bin:${PATH}" >> ${PROFILE}
    echo "`pyenv init --path`" >> ${PROFILE}
    # Install Python 3.8.5
    export TARGET_PYTHON_VERSION="3.8.5"
    pyenv install ${TARGET_PYTHON_VERSION}
    pyenv global ${TARGET_PYTHON_VERSION}
    # Update pip
    echo "Updating pip"
    ${VAGRANT_INSTALL}/versions/${TARGET_PYTHON_VERSION}/bin/python3.8 -m pip install --upgrade pip
    # Install poetry
    echo "Installing poetry"
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
  SHELL
  
  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "cd /vagrant && ./setup_on_vagrant.sh && ./run_gunicorn.sh"}
  end
  
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  
end
