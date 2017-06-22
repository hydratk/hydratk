.. _module_hydra_lib_system:

system
======

This sections contains module documentation of system modules.

auth
^^^^

Module provides methods for user authentication.
Unit tests available at hydratk/lib/system/auth/01_methods_ut.jedi

* check_auth

Method checks authentication credentials. By default it checks against /etc/passwd or /etc/shadow if exists.

config
^^^^^^

Module provides methods for configuration defaults.

* update_htk_vars

Method updates HTK config variables.

* is_virtualized

Method determines if there's virtualized Python environment.

* get_supported_os

Method returns supported os string.

fs
^^

Module provides methods for file operations.
Unit tests available at hydratk/lib/system/fs/01_methods_ut.jedi

* rmkdir

Method creates directory.

* file_get_contents

Method reads file.

* file_put_contents

Method writes to file.

io
^^

Module provides methods for controlled input output.

* cprint

Method prints debug message.

* rprint

Methods writes raw data to the stdio.

mtime
^^^^^

Module provides methods for time operations.
Unit tests available at hydratk/lib/system/mtime/01_methods_ut.jedi

* microtime

Method returns timestamp including microseconds. 

utils
^^^^^

Module provides class Utils with static methods.
Unit tests available at hydratk/lib/system/utils/01_methods_ut.jedi

* module_version

Method returns version of given module using pkg_resources method get_distribution.

* module_loaded

Method checks if given module is already loaded using pkgutil method iter_modules.

* module_exists

Method checks if given module is available in global context.

* module_version_ok

Method checks if current module version is at least minimal version using distutils method StrictVersion.