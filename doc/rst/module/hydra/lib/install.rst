.. _module_hydra_lib_install:

install
=======

This sections contains module documentation of install modules.

command
^^^^^^^

Module provides common installation commands.

* is_install_cmd

Method checks if installation is requested, commands: install, bdist_egg, bdist_wheel.

* get_pck_manager

Method returns installed system package managers: apt-get, yum.

* is_installed

Method checks if system application is installed using command which.

* install_pck

Method installs system package from repository using apt-get or yum.

* create_dir

Method creates directory using mkdir.

* copy_file

Method copies file using cp.

* move_file

Method moves file using mv.

* remove

Method removes file or directory using rm.

* set_rights

Method sets file or directory access rights (inc. recursive rights) using chmod.

* install_pip

Method installs python module using pip.

* uninstall_pip

Method uninstall python module using pip.

task
^^^^

Module provides common installation tasks.

* run_pre_install

Method runs pre-install tasks from configuration.

* run_post_install

Method runs post-install tasks from configuration.

* check_libs

Method checks installed library dependencies

* install_libs

Method installs system libraries from configuration.

* install_modules

Method installs python modules from configuration.

* copy_files

Method copies files from configuration.

* set_access_rights

Methods sets access rights from configuration.

* set_config

Methods sets configuration file. It backups current configuration (file _old) if it differs from default configuration.

* set_manpage

Method sets manual page.

* get_profiles

Method gets module profiles.

uninstall
^^^^^^^^^

Module provides uninstallation tasks.

* run_uninstall

Method handles command htkuninstall. By default it uninstalls hydratk including extensions and libraries.
It supports command option to uninstall requested extension or library only.

* uninstall_ext

Method uninstalls extension via pip and deletes additional files.

* uninstall_lib

Method uninstalls library via pip and deleted additional files.