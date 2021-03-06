# -*- coding: utf-8 -*-

import sys

#Prevent distutils setup functions calls
from setuptools import setup as st_setup
from setuptools import find_packages as st_find_packages

from sys import argv, version_info

sys.path.append('src')
import hydratk.lib.install.task as task
import hydratk.lib.system.config as syscfg

try:
    os_info = syscfg.get_supported_os()
except Exception as exc:
    print(str(exc))
    exit(1)

with open("README.rst", "r") as f:
    readme = f.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]


def version_update(cfg, *args):

    major, minor = version_info[0], version_info[1]
    if os_info['compat'] != 'windows':
        module = 'setproctitle'
        if (major == 2 and minor == 6):
            cfg['modules'].insert(0, {'module': 'importlib', 'version': '>=1.0.4'})
            cfg['libs'][module]['debian']['apt-get'][0] = 'python2.6-dev'
            cfg['libs'][module]['redhat']['yum'][1] = 'python2.6-devel'
            cfg['libs'][module]['fedora']['dnf'][1] = 'python2.6-devel'
            cfg['libs'][module]['suse']['zypper'][0] = 'python2.6-devel'
        elif (major == 3):        
            cfg['libs'][module]['debian']['apt-get'][0] = 'python3-dev'
            cfg['libs'][module]['redhat']['yum'][1] = 'python3-devel'
            cfg['libs'][module]['fedora']['dnf'][1] = 'python3-devel'
            cfg['libs'][module]['suse']['zypper'][0] = 'python3-devel'

""" 
    DEFAULT CONFIG
    Exceptions aka MS Windows dependencies defined bellow
"""
config = {
    'pre_tasks': [
        version_update,        
        task.install_libs,
        task.install_modules
    ],

    'post_tasks': [
        task.set_config,
        task.create_dirs
    ],

    'modules': [        
        {'module': 'pyzmq',        'version': '>=14.7.0'},
        {'module': 'psutil',       'version': '>=3.1.1'},
        {'module': 'pyyaml',       'version': '>=3.11'},
        {'module': 'xtermcolor',   'version': '>=1.3'},
    ],

    'dirs': [
        '{0}/hydratk/dbconfig'.format(syscfg.HTK_VAR_DIR),
        syscfg.HTK_LOG_DIR
    ],

    'files': {
        'config': {
            'etc/hydratk/hydratk.conf': '{0}/etc/hydratk'.format(syscfg.HTK_ROOT_DIR)
        },
        'manpage': 'doc/htk.1'
    },

    'libs': {
        'pyzmq': {
            'debian': {      
                'apt-get': [                    
                    'g++',
                    'libzmq-dev'
                ],
                'check' : {
                    'g++' : {
                        'cmd' : 'which g++',
                        'errmsg' : 'Required g++ compiler not found in path'
                    },                   
                    'libzmq-dev' : {
                        'cmd' : '/sbin/ldconfig -p | grep libzmq || locate libzmq',
                        'errmsg' : 'Unable to locate shared library libzmq'
                    }                           
                }           
            },
            'redhat': {                 
                'yum': [
                    'epel-release',    
                    'gcc-c++',
                    'zeromq'
                ],
                'check' : {
                    'epel-release' : {
                        'cmd' : 'yum list installed | grep epel-release',
                        'errmsg' : 'Unable to locate package epel-release not found'
                    },       
                    'gcc-c++' : {
                        'cmd' : 'which g++',
                        'errmsg' : 'Required g++ compiler not found in path'
                    },
                    'zeromq' : {
                        'cmd' : '/sbin/ldconfig -p | grep libzmq || locate libzmq',
                        'errmsg' : 'Unable to locate shared library libzmq'
                    }                                                 
                }        
            },
            'fedora': {
                'dnf': [
                    'gcc-c++',
                    'zeromq'
                ],
                'check' : {
                    'gcc-c++' : {
                        'cmd' : 'which g++',
                        'errmsg' : 'Required g++ compiler not found in path'
                    },
                    'zeromq' : {
                        'cmd' : '/sbin/ldconfig -p | grep libzmq || locate libzmq',
                        'errmsg' : 'Unable to locate shared library libzmq'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'gcc-c++',
                    'zeromq-devel'
                ],
                'check' : {
                    'gcc-c++' : {
                        'cmd' : 'which g++',
                        'errmsg' : 'Required g++ compiler not found in path'
                    },
                    'zeromq-devel' : {
                        'cmd' : '/sbin/ldconfig -p | grep libzmq || locate libzmq',
                        'errmsg' : 'Unable to locate shared library libzmq'
                    }
                }
            },
            'gentoo': {
                'emerge': [
                    'g++'
                ],
                'check' : {
                    'g++' : {
                        'cmd' : 'which g++',
                        'errmsg' : 'Required g++ compiler not found in path'
                    }
                }
            },
            'arch': {
                'pacman': [
                    'g++'
                ],
                'check' : {
                    'g++' : {
                        'cmd' : 'which g++',
                        'errmsg' : 'Required g++ compiler not found in path'
                    }
                }
            }
        }
    },

    'rights': {
        '{0}/hydratk'.format(syscfg.HTK_ETC_DIR) : 'a+r',
        '{0}/hydratk'.format(syscfg.HTK_VAR_DIR) : 'a+rwx'
    }
}
if os_info['compat'] != 'windows':
    config['modules'].extend(
            [
              {'module': 'setproctitle', 'version': '>=1.1.9'}
            ]
    )
    config['libs'].update(
      { 
        'setproctitle': {
            'debian': {              
                'apt-get': [
                    'python-dev',
                    'gcc',
                    'wget',
                    'bzip2',
                    'tar'
                ],
                'check' : {
                    'gcc' : { 
                        'cmd' : 'which gcc',
                        'errmsg' : 'Required gcc compiler not found in path'
                    }, 
                    'wget' : { 
                        'cmd' : 'which wget',
                        'errmsg' : 'Required wget downloader not found in path'
                    }, 
                    'bzip2' : { 
                        'cmd' : 'which bzip2',
                        'errmsg' : 'Required bzip2 compressor not found in path'
                    }, 
                    'tar' : { 
                        'cmd' : 'which tar',
                        'errmsg' : 'Required tar compressor not found in path'
                    },                                                                                                   
                    'python-dev' : { 
                        'cmd' : 'dpkg --get-selections | grep python-dev',
                        'errmsg' : 'Unable to locate package python-dev'
                    },  
                    'python2.6-dev' : {
                        'cmd' : 'dpkg --get-selections | grep python2.6-dev',
                        'errmsg' : 'Unable to locate package python2.6-dev'
                    },
                    'python3-dev' : {
                        'cmd' : 'dpkg --get-selections | grep python3-dev',
                        'errmsg' : 'Unable to locate package python3-dev'
                    }
                 }           
            },
            'redhat': {                        
                'yum': [
                    'redhat-rpm-config',
                    'python-devel',
                    'gcc',
                    'wget',
                    'bzip2',
                    'tar'
                ],
                'check' : {
                    'gcc' : { 
                        'cmd' : 'which gcc',
                        'errmsg' : 'Required gcc compiler not found in path'
                    },
                    'wget' : { 
                        'cmd' : 'which wget',
                        'errmsg' : 'Required wget downloader not found in path'
                    },
                    'bzip2' : { 
                        'cmd' : 'which bzip2',
                        'errmsg' : 'Required bzip2 compressor not found in path'
                    },
                    'tar' : { 
                        'cmd' : 'which tar',
                        'errmsg' : 'Required tar compressor not found in path'
                    },                                                                                                          
                    'redhat-rpm-config' : { 
                        'cmd' : 'yum list installed | grep redhat-rpm-config',
                        'errmsg' : 'Unable to locate package redhat-rpm-config not found'
                    },
                    'python-devel' : { 
                        'cmd' : 'yum list installed | grep python-devel',
                        'errmsg' : 'Unable to locate package python-devel'
                    },  
                    'python2.6-devel' : {
                        'cmd' : 'yum list installed | grep python2.6-devel',
                        'errmsg' : 'Unable to locate package python2.6-devel'
                    },
                    'python3-devel' : {
                        'cmd' : 'yum list installed | grep python3-devel',
                        'errmsg' : 'Unable to locate package python3-devel'
                    }
                }           
            },
            'fedora': {
                'dnf': [
                    'redhat-rpm-config',
                    'python-devel',
                    'gcc',
                    'wget',
                    'bzip2',
                    'tar'
                ],
                'check' : {
                    'gcc' : {
                        'cmd' : 'which gcc',
                        'errmsg' : 'Required gcc compiler not found in path'
                    },
                    'wget' : {
                        'cmd' : 'which wget',
                        'errmsg' : 'Required wget downloader not found in path'
                    },
                    'bzip2' : {
                        'cmd' : 'which bzip2',
                        'errmsg' : 'Required bzip2 compressor not found in path'
                    },
                    'tar' : {
                        'cmd' : 'which tar',
                        'errmsg' : 'Required tar compressor not found in path'
                    },
                    'redhat-rpm-config' : {
                        'cmd' : 'dnf list installed | grep redhat-rpm-config',
                        'errmsg' : 'Unable to locate package redhat-rpm-config not found'
                    },
                    'python-devel' : {
                        'cmd' : 'dnf list installed | grep python-devel',
                        'errmsg' : 'Unable to locate package python-devel'
                    },
                    'python2.6-devel' : {
                        'cmd' : 'dnf list installed | grep python2.6-devel',
                        'errmsg' : 'Unable to locate package python2.6-devel'
                    },
                    'python3-devel' : {
                        'cmd' : 'dnf list installed | grep python3-devel',
                        'errmsg' : 'Unable to locate package python3-devel'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'python-devel',
                    'gcc',
                    'wget',
                    'bzip2',
                    'tar'
                ],
                'check' : {
                    'gcc' : {
                        'cmd' : 'which gcc',
                        'errmsg' : 'Required gcc compiler not found in path'
                    },
                    'wget' : {
                        'cmd' : 'which wget',
                        'errmsg' : 'Required wget downloader not found in path'
                    },
                    'bzip2' : {
                        'cmd' : 'which bzip2',
                        'errmsg' : 'Required bzip2 compressor not found in path'
                    },
                    'tar' : {
                        'cmd' : 'which tar',
                        'errmsg' : 'Required tar compressor not found in path'
                    },
                    'python-devel' : {
                        'cmd' : 'rpm -qa | grep python-devel',
                        'errmsg' : 'Unable to locate package python-devel'
                    },
                    'python2.6-devel' : {
                        'cmd' : 'rpm -qa | grep python2.6-devel',
                        'errmsg' : 'Unable to locate package python2.6-devel'
                    },
                    'python3-devel' : {
                        'cmd' : 'rpm -qa | grep python3-devel',
                        'errmsg' : 'Unable to locate package python3-devel'
                    }
                }
            },
            'gentoo': {
                'emerge': [
                    'gcc',
                    'wget',
                    'bzip2',
                    'tar'
                ],
                'check' : {
                    'gcc' : {
                        'cmd' : 'which gcc',
                        'errmsg' : 'Required gcc compiler not found in path'
                    },
                    'wget' : {
                        'cmd' : 'which wget',
                        'errmsg' : 'Required wget downloader not found in path'
                    },
                    'bzip2' : {
                        'cmd' : 'which bzip2',
                        'errmsg' : 'Required bzip2 compressor not found in path'
                    },
                    'tar' : {
                        'cmd' : 'which tar',
                        'errmsg' : 'Required tar compressor not found in path'
                    }
                 }
            },
            'arch': {
                'pacman': [
                    'gcc',
                    'wget',
                    'bzip2',
                    'tar'
                ],
                'check' : {
                    'gcc' : {
                        'cmd' : 'which gcc',
                        'errmsg' : 'Required gcc compiler not found in path'
                    },
                    'wget' : {
                        'cmd' : 'which wget',
                        'errmsg' : 'Required wget downloader not found in path'
                    },
                    'bzip2' : {
                        'cmd' : 'which bzip2',
                        'errmsg' : 'Required bzip2 compressor not found in path'
                    },
                    'tar' : {
                        'cmd' : 'which tar',
                        'errmsg' : 'Required tar compressor not found in path'
                    }
                 }
            }
        }
      }        
    )

    config['post_tasks'].extend(
       [
        task.set_access_rights,
        task.set_manpage
       ]
    )
    
task.run_pre_install(argv, config)

entry_points = {
    'console_scripts': [
        'htk = hydratk.core.bootstrapper:run_app',        
        'htkuninstall = hydratk.lib.install.uninstall:run_uninstall'
    ]
}

st_setup(
    name='hydratk',
    version='0.6.0',
    description='Fully extendable object oriented application toolkit with nice modular architecture',
    long_description=readme,
    author='Petr Czaderna, HydraTK team',
    author_email='pc@hydratk.org, team@hydratk.org',
    url='http://www.hydratk.org',
    license='BSD',
    packages=st_find_packages('src'),
    package_dir={'': 'src'},
    classifiers=classifiers,
    zip_safe=False,
    entry_points=entry_points,
    keywords='toolkit,utilities,testing,analysis',
    requires_python='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
    platforms='Linux,FreeBSD,Windows'
)

task.run_post_install(argv, config)
