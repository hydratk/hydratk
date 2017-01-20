# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sys import argv
import install.script as inst

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
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython", 
    "Programming Language :: Python :: Implementation :: PyPy",  
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]

inst.run_pre_install(argv, inst.config)

entry_points = {
                'console_scripts': [
                    'htk = hydratk.core.bootstrapper:run_app',
                    'htkprof = hydratk.core.bootstrapper:run_app_prof'             
                ]
               } 
     
setup(
      name='hydratk',
      version='0.5.0a.dev2',
      description='Fully extendable object oriented application toolkit with nice modular architecture',
      long_description=readme,
      author='Petr Czaderna, HydraTK team',
      author_email='pc@hydratk.org, team@hydratk.org',
      url='http://www.hydratk.org',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'' : 'src'},
      classifiers=classifiers,
      zip_safe=False,      
      entry_points=entry_points,
      keywords='toolkit,utilities,testing,analysis',
      requires_python='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
      platforms='Linux'
     )

inst.run_post_install(argv, inst.config)