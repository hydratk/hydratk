from setuptools import setup


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
];

packages = [
          'hydratk',
          'hydratk.core',
          'hydratk.lib.array',
          'hydratk.lib.compat',
          'hydratk.lib.console',
          'hydratk.lib.debugging',
          'hydratk.lib.exceptions',
          'hydratk.lib.messaging',
          'hydratk.lib.number',
          'hydratk.lib.profiling',
          'hydratk.lib.string',
          'hydratk.lib.system',
          'hydratk.lib.translation',
          'hydratk.extensions.benchmark',
          'hydratk.extensions.wings',
          'hydratk.translation'          
         ];
         
requires = [
           'setproctitle',
           'xtermcolor',
           'pyzmq',
           'pyyaml',
           'psutil',
           'cherrypy',
           'tornado',
         ];                
         
setup(
      name='HydraTk',
      version='0.1.0',
      description='Fully extendable object oriented application toolkit with nice modular architecture',
      long_description=readme,
      author='Petr Czaderna',
      author_email='pc@hydratk.org',
      url='http://www.hydratk.org',
      license='BSD',
      packages=packages,
      install_requires=requires,
      package_dir={'' : 'src'},
      classifiers=classifiers,
      zip_safe=False
     )