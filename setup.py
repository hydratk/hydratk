from setuptools import setup, find_packages


with open("README.rst", "r") as f:
    readme = f.readlines()
    
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",   
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",    
    "Programming Language :: Python :: Implementation :: PyPy",    
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]

         
requires = [
           'setproctitle',
           'xtermcolor',
           'pyzmq',
           'pytz'
           'pyyaml',
           'psutil',
           'cherrypy',
           'tornado',
           'paramiko',
           'tftpy',
           'pycurl',
           'cx_Oracle',
           'MySQLdb',
           'psycopg2',
           'httplib2',
           'jsonlib2',
           'lxml',
           'suds'
         ]
         
data_files=[
            ('/etc/hydratk', ['etc/hydratk/hydratk.conf'])            
           ]

entry_points={
          'console_scripts': [
              'htk = hydratk.core.bootstrapper:run_app',            
          ]
      }                                     
         
setup(
      name='HydraTK',
      version='0.1.0a.dev4',
      description='Fully extendable object oriented application toolkit with nice modular architecture',
      long_description=readme,
      author='Petr Czaderna, HydraTK Team',
      author_email='team@hydratk.org',
      url='http://www.hydratk.org',
      license='BSD',
      packages=find_packages('src'),
      install_requires=requires,
      package_dir={'' : 'src'},
      classifiers=classifiers,
      zip_safe=False,
      data_files=data_files,
      entry_points=entry_points
     )