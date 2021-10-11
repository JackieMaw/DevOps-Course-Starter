
Vagrant.configure("2") do |config|

  config.vm.box = "hashicorp/bionic64"

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
	export PROFILE=/home/vagrant/.profile
    export INSTALL_ROOT="/home/vagrant"
    cd ${INSTALL_ROOT}
	    sudo apt-get update
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
    export VAGRANT_INSTALL=${INSTALL_ROOT}/.pyenv
    git clone https://github.com/pyenv/pyenv.git ${VAGRANT_INSTALL}
    export PATH=${VAGRANT_INSTALL}/bin:${PATH}
    echo "" >> ${PROFILE}
    echo "# set Vagrant env vars" >> ${PROFILE}
    echo "export VAGRANT_INSTALL=${VAGRANT_INSTALL}" >> ${PROFILE}
    echo "export PATH=${VAGRANT_INSTALL}/bin:${PATH}" >> ${PROFILE}
    echo "`pyenv init --path`" >> ${PROFILE}
    export TARGET_PYTHON_VERSION="3.8.5"
    pyenv install ${TARGET_PYTHON_VERSION}
    pyenv global ${TARGET_PYTHON_VERSION}
    echo "Updating pip"
    ${VAGRANT_INSTALL}/versions/${TARGET_PYTHON_VERSION}/bin/python3.8 -m pip install --upgrade pip
    echo "Installing poetry"
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
  SHELL
  
  config.trigger.after :up do |trigger|
	 trigger.name = "Launching App"
	 trigger.info = "Running the TODO app setup script"
	 trigger.run_remote = {privileged: false, inline: <<-SHELL
      cd /vagrant
      poetry install
      cd /vagrant/todo_app
      echo "Launching the application in the background..."
      nohup poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
   SHELL
	 }
  end  
  
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  
end