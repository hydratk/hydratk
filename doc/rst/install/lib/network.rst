.. install_lib_network:

Network
=======

You have 2 options how to install Network library.

PIP
^^^

Install it via Python package manager PIP

  .. code-block:: bash
  
     $ sudo pip install hydratk-lib-network 

GitHub
^^^^^^

Download the source code from GitHub and install it manually.

  .. code-block:: bash
  
     $ git clone https://git.hydratk.org/hydratk-lib-network.git
     $ cd ./hydratk-lib-network
     $ sudo python setup.py install
     
Installation
^^^^^^^^^^^^

Oracle client is not bundled with library and must be installed individually.
Setup script checks if environment variable ORACLE_HOME is set. If not the module cx_Oracle is excluded.
When you install Oracle, you can update library and cx_Oracle will be installed.

Java virtual machine is not bundled with library and must be installed individually.
Setup script checks if environment variable JAVA_HOME is set. If not the module JPype1 is excluded.
When you install JVM, you can update library and JPype1 including jar files will be installed. 

See installation example for Linux based on Debian distribution. 

  .. note::
  
     The system is clean therefore external libraries will be also installed (several MBs will be downloaded)
     You can see strange log messages which are out of hydratk control. 
     
  .. code-block:: bash
  
     **************************************
     *    HydraTK Network installation    *
     **************************************
     **************************************
     *     Running pre-install tasks      *
     **************************************

     *** Running task: install_libs_from_repo ***

     Installing package: python-lxml
     Installing package: libfontconfig
     Installing package: libffi-dev
     Installing package: libssl-dev
     Installing package: libaio1
     Installing package: libaio-dev
     Installing package: mysql-devel
     Installing package: python-mysqldb
     Installing package: libldap2-dev
     Installing package: libsasl2-dev
     Installing package: libssl-dev
     Installing package: python-pycurl
     Installing package: libcurl4-openssl-dev
     Installing package: python-psycopg2

     *** Running task: install_java ***

     Java has not been detected. If you want to use HydraTK Java bridge, install Java first.

     *** Running task: install_oracle ***

     Oracle has not been detected. If you want to use HydraTK Oracle client, install Oracle first.
     
     running install
     running bdist_egg
     running egg_info
     creating src/hydratk_lib_network.egg-info
     writing requirements to src/hydratk_lib_network.egg-info/requires.txt
     writing src/hydratk_lib_network.egg-info/PKG-INFO
     writing top-level names to src/hydratk_lib_network.egg-info/top_level.txt
     writing dependency_links to src/hydratk_lib_network.egg-info/dependency_links.txt
     writing manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     reading manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     writing manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     copying src/hydratk/__init__.py -> build/lib.linux-x86_64-2.7/hydratk
     ... 
     
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/__init__.py to __init__.pyc
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/lib/__init__.py to __init__.pyc
     ... 
     
     creating build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/requires.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     creating dist
     creating 'dist/hydratk_lib_network-0.1.0-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk_lib_network-0.1.0-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk_lib_network-0.1.0-py2.7.egg
     Extracting hydratk_lib_network-0.1.0-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk-lib-network 0.1.0 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/hydratk_lib_network-0.1.0-py2.7.egg
     Processing dependencies for hydratk-lib-network==0.1.0
     Searching for tftpy>=0.6.2
     Reading https://pypi.python.org/simple/tftpy/
     Best match: tftpy 0.6.2
     Downloading https://pypi.python.org/packages/7d/a5/e246b93d0996264f80c54af706bda111b1547cef6def52ecb05183263af7/tftpy-0.6.2.tar.gz#md5=199c48ca8ea8975170596eb5da109514
     Processing tftpy-0.6.2.tar.gz
     Writing /tmp/easy_install-sQqEPy/tftpy-0.6.2/setup.cfg
     Running tftpy-0.6.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-sQqEPy/tftpy-0.6.2/egg-dist-tmp-wn5cyI
     Moving tftpy-0.6.2-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding tftpy 0.6.2 to easy-install.pth file
     Installing tftpy_server.py script to /usr/local/bin
     Installing tftpy_client.py script to /usr/local/bin

     Installed /usr/local/lib/python2.7/dist-packages/tftpy-0.6.2-py2.7.egg
     Searching for suds>=0.4
     Reading https://pypi.python.org/simple/suds/
     Best match: suds 0.4
     Downloading https://pypi.python.org/packages/bc/d6/960acce47ee6f096345fe5a7d9be7708135fd1d0713571836f073efc7393/suds-0.4.tar.gz#md5=b7502de662341ed7275b673e6bd73191
     Processing suds-0.4.tar.gz
     Writing /tmp/easy_install-6wUY6f/suds-0.4/setup.cfg
     Running suds-0.4/setup.py -q bdist_egg --dist-dir /tmp/easy_install-6wUY6f/suds-0.4/egg-dist-tmp-oMf8q1
     Moving suds-0.4-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding suds 0.4 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/suds-0.4-py2.7.egg
     Searching for selenium>=2.46.1
     Reading https://pypi.python.org/simple/selenium/
     Best match: selenium 2.53.5
     Downloading https://pypi.python.org/packages/41/ff/d77fd45739a2290da74ba314182fcfbe98b4e617e89b973bc5c667444334/selenium-2.53.5.tar.gz#md5=c7e40c360d73e267234e166f252f574c
     Processing selenium-2.53.5.tar.gz
     Writing /tmp/easy_install-BtRRl0/selenium-2.53.5/setup.cfg
     Running selenium-2.53.5/setup.py -q bdist_egg --dist-dir /tmp/easy_install-BtRRl0/selenium-2.53.5/egg-dist-tmp-gY5prL
     creating /usr/local/lib/python2.7/dist-packages/selenium-2.53.5-py2.7.egg
     Extracting selenium-2.53.5-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding selenium 2.53.5 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/selenium-2.53.5-py2.7.egg
     Searching for scapy>=2.3.1
     Reading https://pypi.python.org/simple/scapy/
     Best match: scapy 2.3.2
     Downloading https://pypi.python.org/packages/6d/72/c055abd32bcd4ee6b36ef8e9ceccc2e242dea9b6c58fdcf2e8fd005f7650/scapy-2.3.2.tar.gz#md5=b8ca06ca3b475bd01ba6cf5cdc5619af
     Processing scapy-2.3.2.tar.gz
     Writing /tmp/easy_install-5UQgtO/scapy-2.3.2/setup.cfg
     Running scapy-2.3.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-5UQgtO/scapy-2.3.2/egg-dist-tmp-nZc91g
     creating /usr/local/lib/python2.7/dist-packages/scapy-2.3.2-py2.7.egg
     Extracting scapy-2.3.2-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding scapy 2.3.2 to easy-install.pth file
     Installing UTscapy script to /usr/local/bin
     Installing scapy script to /usr/local/bin

     Installed /usr/local/lib/python2.7/dist-packages/scapy-2.3.2-py2.7.egg
     Searching for python-ntlm>=1.1.0
     Reading https://pypi.python.org/simple/python-ntlm/
     Best match: python-ntlm 1.1.0
     Downloading https://pypi.python.org/packages/10/0e/e7d7e1653852fe440f0f66fa65d14dd21011d894690deafe4091258ea855/python-ntlm-1.1.0.tar.gz#md5=c1b036401a29dd979ee56d48a2267686
     Processing python-ntlm-1.1.0.tar.gz
     Writing /tmp/easy_install-R2s5CN/python-ntlm-1.1.0/setup.cfg
     Running python-ntlm-1.1.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-R2s5CN/python-ntlm-1.1.0/egg-dist-tmp-IAw6xc
     creating /usr/local/lib/python2.7/dist-packages/python_ntlm-1.1.0-py2.7.egg
     Extracting python_ntlm-1.1.0-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding python-ntlm 1.1.0 to easy-install.pth file
     Installing ntlm_example_extended script to /usr/local/bin
     Installing ntlm_example_simple script to /usr/local/bin

     Installed /usr/local/lib/python2.7/dist-packages/python_ntlm-1.1.0-py2.7.egg
     Searching for python-ldap>=2.4.25
     Reading https://pypi.python.org/simple/python-ldap/
     Best match: python-ldap 2.4.25
     Downloading https://pypi.python.org/packages/9b/1a/f2bc7ebf2f0b21d78d7cc2b5c283fb265397912cd63c4b53c83223ebcac9/python-ldap-2.4.25.tar.gz#md5=21523bf21dbe566e0259030f66f7a487
     Processing python-ldap-2.4.25.tar.gz
     Writing /tmp/easy_install-K4VVWy/python-ldap-2.4.25/setup.cfg
     Running python-ldap-2.4.25/setup.py -q bdist_egg --dist-dir /tmp/easy_install-K4VVWy/python-ldap-2.4.25/egg-dist-tmp-E95mtz
     defines: HAVE_SASL HAVE_TLS HAVE_LIBLDAP_R
     extra_compile_args: 
     extra_objects: 
     include_dirs: /usr/include /usr/include/sasl /usr/local/include /usr/local/include/sasl
     library_dirs: /usr/lib /usr/lib64 /usr/local/lib /usr/local/lib64
     libs: ldap_r
     creating /usr/local/lib/python2.7/dist-packages/python_ldap-2.4.25-py2.7-linux-x86_64.egg
     Extracting python_ldap-2.4.25-py2.7-linux-x86_64.egg to /usr/local/lib/python2.7/dist-packages
     Adding python-ldap 2.4.25 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/python_ldap-2.4.25-py2.7-linux-x86_64.egg
     Searching for pyexcel-ods3>=0.1.1
     Reading https://pypi.python.org/simple/pyexcel-ods3/
     Best match: pyexcel-ods3 0.2.0
     Downloading https://pypi.python.org/packages/e0/84/8ce15c7b4ea392fb560cd43a6de0cd8b5f4803832eb26e5b141c34e03da5/pyexcel-ods3-0.2.0.zip#md5=1985c2f3ceb9337b1bcc9503660b8d45
     Processing pyexcel-ods3-0.2.0.zip
     Writing /tmp/easy_install-ELIz19/pyexcel-ods3-0.2.0/setup.cfg
     Running pyexcel-ods3-0.2.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-ELIz19/pyexcel-ods3-0.2.0/egg-dist-tmp-B778cU
     creating /usr/local/lib/python2.7/dist-packages/pyexcel_ods3-0.2.0-py2.7.egg
     Extracting pyexcel_ods3-0.2.0-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding pyexcel-ods3 0.2.0 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/pyexcel_ods3-0.2.0-py2.7.egg
     Searching for pyexcel-xlsx>=0.1.0
     Reading https://pypi.python.org/simple/pyexcel-xlsx/
     Best match: pyexcel-xlsx 0.2.0
     Downloading https://pypi.python.org/packages/0e/79/14739d317451e8ceed934075c49541336d8c3d0ddad53e946bffdb47ac6d/pyexcel-xlsx-0.2.0.zip#md5=9139b9bdcaf2f185abab31337a40cf05
     Processing pyexcel-xlsx-0.2.0.zip
     Writing /tmp/easy_install-mP24Hm/pyexcel-xlsx-0.2.0/setup.cfg
     Running pyexcel-xlsx-0.2.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-mP24Hm/pyexcel-xlsx-0.2.0/egg-dist-tmp-0wPB4E
     creating /usr/local/lib/python2.7/dist-packages/pyexcel_xlsx-0.2.0-py2.7.egg
     Extracting pyexcel_xlsx-0.2.0-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding pyexcel-xlsx 0.2.0 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/pyexcel_xlsx-0.2.0-py2.7.egg
     Searching for pyexcel>=0.2.0
     Reading https://pypi.python.org/simple/pyexcel/
     Best match: pyexcel 0.2.2
     Downloading https://pypi.python.org/packages/ae/bb/b4f31f93be6a283816c89fa6fb2608bca58aac7aeeb4df9d46da956389d8/pyexcel-0.2.2.zip#md5=a939ea1841343d533fb31332dcb66ccf
     Processing pyexcel-0.2.2.zip
     Writing /tmp/easy_install-5yizrr/pyexcel-0.2.2/setup.cfg
     Running pyexcel-0.2.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-5yizrr/pyexcel-0.2.2/egg-dist-tmp-YKtt8y
     creating /usr/local/lib/python2.7/dist-packages/pyexcel-0.2.2-py2.7.egg
     Extracting pyexcel-0.2.2-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding pyexcel 0.2.2 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/pyexcel-0.2.2-py2.7.egg
     Searching for pycurl>=7.19.5.1
     Reading https://pypi.python.org/simple/pycurl/
     Best match: pycurl 7.43.0
     Downloading https://pypi.python.org/packages/12/3f/557356b60d8e59a1cce62ffc07ecc03e4f8a202c86adae34d895826281fb/pycurl-7.43.0.tar.gz#md5=c94bdba01da6004fa38325e9bd6b9760
     Processing pycurl-7.43.0.tar.gz
     Writing /tmp/easy_install-9T9U7x/pycurl-7.43.0/setup.cfg
     Running pycurl-7.43.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-9T9U7x/pycurl-7.43.0/egg-dist-tmp-xiRz7A
     Using curl-config (libcurl 7.38.0)
     Moving pycurl-7.43.0-py2.7-linux-x86_64.egg to /usr/local/lib/python2.7/dist-packages
     Adding pycurl 7.43.0 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/pycurl-7.43.0-py2.7-linux-x86_64.egg
     Searching for paramiko>=1.16.0
     Reading https://pypi.python.org/simple/paramiko/
     Best match: paramiko 2.0.1
     Downloading https://pypi.python.org/packages/b5/dd/cc2b8eb360e3db2e65ad5adf8cb4fd57493184e3ce056fd7625e9c387bfa/paramiko-2.0.1.tar.gz#md5=c00d63b34dcf74649216bdc8875e1ebe
     Processing paramiko-2.0.1.tar.gz
     Writing /tmp/easy_install-b8mU86/paramiko-2.0.1/setup.cfg
     Running paramiko-2.0.1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-b8mU86/paramiko-2.0.1/egg-dist-tmp-LUSVnY
     Moving paramiko-2.0.1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding paramiko 2.0.1 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/paramiko-2.0.1-py2.7.egg
     Searching for jsonlib2>=1.5.2
     Reading https://pypi.python.org/simple/jsonlib2/
     Best match: jsonlib2 1.5.2
     Downloading https://pypi.python.org/packages/0e/1d/745b4e69ca0710215f7291ebbdfcdc95896dec7e196312b29d5a7c606038/jsonlib2-1.5.2.tar.gz#md5=f650c6979c04ed128e76edaa9ba50323
     Processing jsonlib2-1.5.2.tar.gz
     Writing /tmp/easy_install-Ilsorx/jsonlib2-1.5.2/setup.cfg
     Running jsonlib2-1.5.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-Ilsorx/jsonlib2-1.5.2/egg-dist-tmp-lYLRzo
     Moving jsonlib2-1.5.2-py2.7-linux-x86_64.egg to /usr/local/lib/python2.7/dist-packages
     Adding jsonlib2 1.5.2 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/jsonlib2-1.5.2-py2.7-linux-x86_64.egg
     Searching for httplib2>=0.9.1
     Reading https://pypi.python.org/simple/httplib2/
     Best match: httplib2 0.9.2
     Downloading https://pypi.python.org/packages/ff/a9/5751cdf17a70ea89f6dde23ceb1705bfb638fd8cee00f845308bf8d26397/httplib2-0.9.2.tar.gz#md5=bd1b1445b3b2dfa7276b09b1a07b7f0e
     Processing httplib2-0.9.2.tar.gz
     Writing /tmp/easy_install-_S0t9B/httplib2-0.9.2/setup.cfg
     Running httplib2-0.9.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-_S0t9B/httplib2-0.9.2/egg-dist-tmp-YmKyl_
     creating /usr/local/lib/python2.7/dist-packages/httplib2-0.9.2-py2.7.egg
     Extracting httplib2-0.9.2-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding httplib2 0.9.2 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/httplib2-0.9.2-py2.7.egg
     Searching for ezodf>=0.3.2
     Reading https://pypi.python.org/simple/ezodf/
     Best match: ezodf 0.3.2
     Downloading https://pypi.python.org/packages/6f/c5/e966935c26d58d7e3d962270be61be972409084374d4093f478d1f82e8af/ezodf-0.3.2.tar.gz#md5=b12670b60b49d3c35338fd46493071fc
     Processing ezodf-0.3.2.tar.gz
     Writing /tmp/easy_install-frYacS/ezodf-0.3.2/setup.cfg
     Running ezodf-0.3.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-frYacS/ezodf-0.3.2/egg-dist-tmp-klN38K
     Moving ezodf-0.3.2-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding ezodf 0.3.2 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/ezodf-0.3.2-py2.7.egg
     Searching for pyexcel-io>=0.1.0
     Reading https://pypi.python.org/simple/pyexcel-io/
     Best match: pyexcel-io 0.2.0
     Downloading https://pypi.python.org/packages/43/39/8f2cea9f97ca057da858565347070ee1aa0f748f1232f00d9370c7ab5ff2/pyexcel-io-0.2.0.zip#md5=2f2ea9e662e1ad541dea96f8259fb9f8
     Processing pyexcel-io-0.2.0.zip
     Writing /tmp/easy_install-RDntqz/pyexcel-io-0.2.0/setup.cfg
     Running pyexcel-io-0.2.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-RDntqz/pyexcel-io-0.2.0/egg-dist-tmp-wtesRt
     creating /usr/local/lib/python2.7/dist-packages/pyexcel_io-0.2.0-py2.7.egg
     Extracting pyexcel_io-0.2.0-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding pyexcel-io 0.2.0 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/pyexcel_io-0.2.0-py2.7.egg
     Searching for openpyxl>=2.2.2
     Reading https://pypi.python.org/simple/openpyxl/
     Best match: openpyxl 2.4.0b1
     Downloading https://pypi.python.org/packages/25/69/7976ba24d2b532e96157623daa8de4bbcad23e0761b3062d5e38775577d5/openpyxl-2.4.0-b1.tar.gz#md5=f56975d698cbfa619a8c99ddce41b142
     Processing openpyxl-2.4.0-b1.tar.gz
     Writing /tmp/easy_install-k8v1Hj/openpyxl-2.4.0-b1/setup.cfg
     Running openpyxl-2.4.0-b1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-k8v1Hj/openpyxl-2.4.0-b1/egg-dist-tmp-qT0klj
     creating /usr/local/lib/python2.7/dist-packages/openpyxl-2.4.0b1-py2.7.egg
     Extracting openpyxl-2.4.0b1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding openpyxl 2.4.0b1 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/openpyxl-2.4.0b1-py2.7.egg
     Searching for texttable>=0.8.1
     Reading https://pypi.python.org/simple/texttable/
     Best match: texttable 0.8.4
     Downloading https://pypi.python.org/packages/f5/5e/47cbc50187ca719a39ce4838182c6126487ca62ddd299bc34cafb94260fe/texttable-0.8.4.tar.gz#md5=6335edbe1bb4edacce7c2f76195f6212
     Processing texttable-0.8.4.tar.gz
     Writing /tmp/easy_install-yv2sZb/texttable-0.8.4/setup.cfg
     Running texttable-0.8.4/setup.py -q bdist_egg --dist-dir /tmp/easy_install-yv2sZb/texttable-0.8.4/egg-dist-tmp-W9xfuS
     Moving texttable-0.8.4-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding texttable 0.8.4 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/texttable-0.8.4-py2.7.egg
     Searching for pyasn1>=0.1.7
     Reading https://pypi.python.org/simple/pyasn1/
     Best match: pyasn1 0.1.9
     Downloading https://pypi.python.org/packages/c3/ea/03328a42adfc16a1babbe334ad969f6e27862bcaff9576444d423d2c9257/pyasn1-0.1.9-py2.7.egg#md5=08eef0e822233609f6cad55b419ae00c
     Processing pyasn1-0.1.9-py2.7.egg
     Moving pyasn1-0.1.9-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding pyasn1 0.1.9 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/pyasn1-0.1.9-py2.7.egg
     Searching for cryptography>=1.1
     Reading https://pypi.python.org/simple/cryptography/
     Best match: cryptography 1.4
     Downloading https://pypi.python.org/packages/a9/5b/a383b3a778609fe8177bd51307b5ebeee369b353550675353f46cb99c6f0/cryptography-1.4.tar.gz#md5=a9763e3831cc7cdb402c028fac1ceb39
     Processing cryptography-1.4.tar.gz
     Writing /tmp/easy_install-1vJSie/cryptography-1.4/setup.cfg
     Running cryptography-1.4/setup.py -q bdist_egg --dist-dir /tmp/easy_install-1vJSie/cryptography-1.4/egg-dist-tmp-u4prED

     Installed /tmp/easy_install-1vJSie/cryptography-1.4/.eggs/cffi-1.7.0-py2.7-linux-x86_64.egg
     Searching for pycparser
     Reading https://pypi.python.org/simple/pycparser/
     Best match: pycparser 2.14
     Downloading https://pypi.python.org/packages/6d/31/666614af3db0acf377876d48688c5d334b6e493b96d21aa7d332169bee50/pycparser-2.14.tar.gz#md5=a2bc8d28c923b4fe2b2c3b4b51a4f935
     Processing pycparser-2.14.tar.gz
     Writing /tmp/easy_install-1vJSie/cryptography-1.4/temp/easy_install-tWLUc3/pycparser-2.14/setup.cfg
     Running pycparser-2.14/setup.py -q bdist_egg --dist-dir /tmp/easy_install-1vJSie/cryptography-1.4/temp/easy_install-tWLUc3/pycparser-2.14/egg-dist-tmp-jgU6sN
     Moving pycparser-2.14-py2.7.egg to /tmp/easy_install-1vJSie/cryptography-1.4/.eggs

     Installed /tmp/easy_install-1vJSie/cryptography-1.4/.eggs/pycparser-2.14-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/cryptography-1.4-py2.7-linux-x86_64.egg
     Extracting cryptography-1.4-py2.7-linux-x86_64.egg to /usr/local/lib/python2.7/dist-packages
     Adding cryptography 1.4 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/cryptography-1.4-py2.7-linux-x86_64.egg
     Searching for et_xmlfile
     Reading https://pypi.python.org/simple/et_xmlfile/
     Best match: et-xmlfile 1.0.1
     Downloading https://pypi.python.org/packages/22/28/a99c42aea746e18382ad9fb36f64c1c1f04216f41797f2f0fa567da11388/et_xmlfile-1.0.1.tar.gz#md5=f47940fd9d556375420b2e276476cfaf
     Processing et_xmlfile-1.0.1.tar.gz
     Writing /tmp/easy_install-iOc1aY/et_xmlfile-1.0.1/setup.cfg
     Running et_xmlfile-1.0.1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-iOc1aY/et_xmlfile-1.0.1/egg-dist-tmp-k2KJAO
     creating /usr/local/lib/python2.7/dist-packages/et_xmlfile-1.0.1-py2.7.egg
     Extracting et_xmlfile-1.0.1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding et-xmlfile 1.0.1 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/et_xmlfile-1.0.1-py2.7.egg
     Searching for jdcal
     Reading https://pypi.python.org/simple/jdcal/
     Best match: jdcal 1.2
     Downloading https://pypi.python.org/packages/37/36/3199cfb80fcbf4e4df3a43647733d4f429862c6c97aeadd757613b9e6830/jdcal-1.2.tar.gz#md5=ab8d5ba300fd1eb01514f363d19b1eb9
     Processing jdcal-1.2.tar.gz
     Writing /tmp/easy_install-9MWiSd/jdcal-1.2/setup.cfg
     Running jdcal-1.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-9MWiSd/jdcal-1.2/egg-dist-tmp-ulJ2dh
     Moving jdcal-1.2-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding jdcal 1.2 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/jdcal-1.2-py2.7.egg
     Searching for cffi>=1.4.1
     Reading https://pypi.python.org/simple/cffi/
     Best match: cffi 1.7.0
     Downloading https://pypi.python.org/packages/83/3c/00b553fd05ae32f27b3637f705c413c4ce71290aa9b4c4764df694e906d9/cffi-1.7.0.tar.gz#md5=34122a545060cee58bab88feab57006d
     Processing cffi-1.7.0.tar.gz
     Writing /tmp/easy_install-J2PmXK/cffi-1.7.0/setup.cfg
     Running cffi-1.7.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-J2PmXK/cffi-1.7.0/egg-dist-tmp-BtNjuu
     creating /usr/local/lib/python2.7/dist-packages/cffi-1.7.0-py2.7-linux-x86_64.egg
     Extracting cffi-1.7.0-py2.7-linux-x86_64.egg to /usr/local/lib/python2.7/dist-packages
     Adding cffi 1.7.0 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/cffi-1.7.0-py2.7-linux-x86_64.egg
     Searching for ipaddress
     Reading https://pypi.python.org/simple/ipaddress/
     Best match: ipaddress 1.0.16
     Downloading https://pypi.python.org/packages/cd/c5/bd44885274379121507870d4abfe7ba908326cf7bfd50a48d9d6ae091c0d/ipaddress-1.0.16.tar.gz#md5=1e27b62aa20f5b6fc200b2bdbf0d0847
     Processing ipaddress-1.0.16.tar.gz
     Writing /tmp/easy_install-MEdhmf/ipaddress-1.0.16/setup.cfg
     Running ipaddress-1.0.16/setup.py -q bdist_egg --dist-dir /tmp/easy_install-MEdhmf/ipaddress-1.0.16/egg-dist-tmp-xGiJw2
     Moving ipaddress-1.0.16-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding ipaddress 1.0.16 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/ipaddress-1.0.16-py2.7.egg
     Searching for enum34
     Reading https://pypi.python.org/simple/enum34/
     Best match: enum34 1.1.6
     Downloading https://pypi.python.org/packages/e8/26/a6101edcf724453845c850281b96b89a10dac6bd98edebc82634fccce6a5/enum34-1.1.6.zip#md5=61ad7871532d4ce2d77fac2579237a9e
     Processing enum34-1.1.6.zip
     Writing /tmp/easy_install-mwV2vN/enum34-1.1.6/setup.cfg
     Running enum34-1.1.6/setup.py -q bdist_egg --dist-dir /tmp/easy_install-mwV2vN/enum34-1.1.6/egg-dist-tmp-GWdCUi
     Moving enum34-1.1.6-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding enum34 1.1.6 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/enum34-1.1.6-py2.7.egg
     Searching for idna>=2.0
     Reading https://pypi.python.org/simple/idna/
     Best match: idna 2.1
     Downloading https://pypi.python.org/packages/fb/84/8c27516fbaa8147acd2e431086b473c453c428e24e8fb99a1d89ce381851/idna-2.1.tar.gz#md5=f6473caa9c5e0cc1ad3fd5d04c3c114b
     Processing idna-2.1.tar.gz
     Writing /tmp/easy_install-qy944o/idna-2.1/setup.cfg
     Running idna-2.1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-qy944o/idna-2.1/egg-dist-tmp-oAQQUN
     Moving idna-2.1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding idna 2.1 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/idna-2.1-py2.7.egg
     Searching for pycparser
     Reading https://pypi.python.org/simple/pycparser/
     Best match: pycparser 2.14
     Downloading https://pypi.python.org/packages/6d/31/666614af3db0acf377876d48688c5d334b6e493b96d21aa7d332169bee50/pycparser-2.14.tar.gz#md5=a2bc8d28c923b4fe2b2c3b4b51a4f935
     Processing pycparser-2.14.tar.gz
     Writing /tmp/easy_install-SsY9qk/pycparser-2.14/setup.cfg
     Running pycparser-2.14/setup.py -q bdist_egg --dist-dir /tmp/easy_install-SsY9qk/pycparser-2.14/egg-dist-tmp-9YV6JZ
     Moving pycparser-2.14-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding pycparser 2.14 to easy-install.pth file

     Installed /usr/local/lib/python2.7/dist-packages/pycparser-2.14-py2.7.egg
     Searching for psycopg2==2.5.4
     Best match: psycopg2 2.5.4
     Adding psycopg2 2.5.4 to easy-install.pth file

     Using /usr/lib/python2.7/dist-packages
     Searching for MySQL-python==1.2.3
     Best match: MySQL-python 1.2.3
     Adding MySQL-python 1.2.3 to easy-install.pth file

     Using /usr/lib/python2.7/dist-packages
     Searching for lxml==3.4.0
     Best match: lxml 3.4.0
     Adding lxml 3.4.0 to easy-install.pth file

     Using /usr/lib/python2.7/dist-packages
     Searching for hydratk==0.3.0a0.dev1
     Best match: hydratk 0.3.0a0.dev1
     Processing hydratk-0.3.0a0.dev1-py2.7.egg
     hydratk 0.3.0a0.dev1 is already the active version in easy-install.pth
     Installing htkprof script to /usr/local/bin
     Installing htk script to /usr/local/bin

     Using /usr/local/lib/python2.7/dist-packages/hydratk-0.3.0a0.dev1-py2.7.egg
     Searching for setuptools==23.0.0
     Best match: setuptools 23.0.0
     Adding setuptools 23.0.0 to easy-install.pth file
     Installing easy_install-3.5 script to /usr/local/bin
     Installing easy_install script to /usr/local/bin

     Using /usr/lib/python2.7/dist-packages
     Finished processing dependencies for hydratk-lib-network==0.1.0
     
     **************************************
     *     Running post-install tasks     *
     **************************************
     
  .. note::
  
     Libraries are installed using apt-get package manager.
     Module cx_Oracle installs: libaio1, libaio-dev
     Module lxml installs: python-lxml, libxml2-dev, libxslt1-dev, libmysqlclient-dev
     Module MySQL-python installs: mysql-devel, python-mysqldb
     Module paramiko installs: libffi-dev, libssl-dev
     Module psycopg2 installs: python-psycopg2, libpq-dev
     Module pycurl installs: python-pycurl, libcurl4-openssl-dev
     Module python-ldap installs: libldap2-dev, libsasl2-dev, libssl-dev
     Module selenium installs: fontconfig      
           
See installation example for Linux based on Red Hat distribution.

  .. code-block:: bash
  
     **************************************
     *    HydraTK Network installation    *
     **************************************
     **************************************
     *     Running pre-install tasks      *
     **************************************

     *** Running task: install_libs_from_repo ***

     Installing package: python-lxml
     Installing package: fontconfig
     Installing package: libffi-devel
     Installing package: openssl-devel
     Installing package: libaio
     Installing package: mysql-devel
     Installing package: openldap-devel
     Installing package: python-pycurl
     Installing package: libcurl-devel
     Installing package: python-psycopg2

     *** Running task: install_java ***

     Java has not been detected. If you want to use HydraTK Java bridge, install Java first.

     *** Running task: install_oracle ***

     Oracle has not been detected. If you want to use HydraTK Oracle client, install Oracle first.
     
     running install
     running bdist_egg
     running egg_info
     creating src/hydratk_lib_network.egg-info
     writing requirements to src/hydratk_lib_network.egg-info/requires.txt
     writing src/hydratk_lib_network.egg-info/PKG-INFO
     writing top-level names to src/hydratk_lib_network.egg-info/top_level.txt
     writing dependency_links to src/hydratk_lib_network.egg-info/dependency_links.txt
     writing manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     reading manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     writing manifest file 'src/hydratk_lib_network.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib
     creating build/lib/hydratk
     copying src/hydratk/__init__.py -> build/lib/hydratk
     ...
     
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/__init__.py to __init__.pyc
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/lib/bridge/__init__.py to __init__.pyccreating build/bdist.linux-x86_64/egg/EGG-INFO
     ...
     
     copying src/hydratk_lib_network.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/requires.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_lib_network.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     creating dist
     creating 'dist/hydratk_lib_network-0.1.0-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk_lib_network-0.1.0-py2.7.egg
     creating /usr/lib/python2.7/site-packages/hydratk_lib_network-0.1.0-py2.7.egg
     Extracting hydratk_lib_network-0.1.0-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding hydratk-lib-network 0.1.0 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/hydratk_lib_network-0.1.0-py2.7.egg
     Processing dependencies for hydratk-lib-network==0.1.0
     Searching for tftpy>=0.6.2
     Reading https://pypi.python.org/simple/tftpy/
     Best match: tftpy 0.6.2
     Downloading https://pypi.python.org/packages/7d/a5/e246b93d0996264f80c54af706bda111b1547cef6def52ecb05183263af7/tftpy-0.6.2.tar.gz#md5=199c48ca8ea8975170596eb5da109514
     Processing tftpy-0.6.2.tar.gz
     Writing /tmp/easy_install-Lgg8E5/tftpy-0.6.2/setup.cfg
     Running tftpy-0.6.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-Lgg8E5/tftpy-0.6.2/egg-dist-tmp-Rdumrd
     Moving tftpy-0.6.2-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding tftpy 0.6.2 to easy-install.pth file
     Installing tftpy_server.py script to /usr/bin
     Installing tftpy_client.py script to /usr/bin

     Installed /usr/lib/python2.7/site-packages/tftpy-0.6.2-py2.7.egg
     Searching for suds>=0.4
     Reading https://pypi.python.org/simple/suds/
     Best match: suds 0.4
     Downloading https://pypi.python.org/packages/bc/d6/960acce47ee6f096345fe5a7d9be7708135fd1d0713571836f073efc7393/suds-0.4.tar.gz#md5=b7502de662341ed7275b673e6bd73191
     Processing suds-0.4.tar.gz
     Writing /tmp/easy_install-PHUmtk/suds-0.4/setup.cfg
     Running suds-0.4/setup.py -q bdist_egg --dist-dir /tmp/easy_install-PHUmtk/suds-0.4/egg-dist-tmp-dWL7lP
     Moving suds-0.4-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding suds 0.4 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/suds-0.4-py2.7.egg
     Searching for selenium>=2.46.1
     Reading https://pypi.python.org/simple/selenium/
     Best match: selenium 2.53.5
     Downloading https://pypi.python.org/packages/41/ff/d77fd45739a2290da74ba314182fcfbe98b4e617e89b973bc5c667444334/selenium-2.53.5.tar.gz#md5=c7e40c360d73e267234e166f252f574c
     Processing selenium-2.53.5.tar.gz
     Writing /tmp/easy_install-BnG8N0/selenium-2.53.5/setup.cfg
     Running selenium-2.53.5/setup.py -q bdist_egg --dist-dir /tmp/easy_install-BnG8N0/selenium-2.53.5/egg-dist-tmp-GkFP_G
     creating /usr/lib/python2.7/site-packages/selenium-2.53.5-py2.7.egg
     Extracting selenium-2.53.5-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding selenium 2.53.5 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/selenium-2.53.5-py2.7.egg
     Searching for scapy>=2.3.1
     Reading https://pypi.python.org/simple/scapy/
     Best match: scapy 2.3.2
     Downloading https://pypi.python.org/packages/6d/72/c055abd32bcd4ee6b36ef8e9ceccc2e242dea9b6c58fdcf2e8fd005f7650/scapy-2.3.2.tar.gz#md5=b8ca06ca3b475bd01ba6cf5cdc5619af
     Processing scapy-2.3.2.tar.gz
     Writing /tmp/easy_install-lFLd_J/scapy-2.3.2/setup.cfg
     Running scapy-2.3.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-lFLd_J/scapy-2.3.2/egg-dist-tmp-vaZC3i
     creating /usr/lib/python2.7/site-packages/scapy-2.3.2-py2.7.egg
     Extracting scapy-2.3.2-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding scapy 2.3.2 to easy-install.pth file
     Installing scapy script to /usr/bin
     Installing UTscapy script to /usr/bin

     Installed /usr/lib/python2.7/site-packages/scapy-2.3.2-py2.7.egg
     Searching for python-ntlm>=1.1.0
     Reading https://pypi.python.org/simple/python-ntlm/
     Best match: python-ntlm 1.1.0
     Downloading https://pypi.python.org/packages/10/0e/e7d7e1653852fe440f0f66fa65d14dd21011d894690deafe4091258ea855/python-ntlm-1.1.0.tar.gz#md5=c1b036401a29dd979ee56d48a2267686
     Processing python-ntlm-1.1.0.tar.gz
     Writing /tmp/easy_install-f6p9q8/python-ntlm-1.1.0/setup.cfg
     Running python-ntlm-1.1.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-f6p9q8/python-ntlm-1.1.0/egg-dist-tmp-pA4G5J
     creating /usr/lib/python2.7/site-packages/python_ntlm-1.1.0-py2.7.egg
     Extracting python_ntlm-1.1.0-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding python-ntlm 1.1.0 to easy-install.pth file
     Installing ntlm_example_extended script to /usr/bin
     Installing ntlm_example_simple script to /usr/bin

     Installed /usr/lib/python2.7/site-packages/python_ntlm-1.1.0-py2.7.egg
     Searching for python-ldap>=2.4.25
     Reading https://pypi.python.org/simple/python-ldap/
     Best match: python-ldap 2.4.25
     Downloading https://pypi.python.org/packages/9b/1a/f2bc7ebf2f0b21d78d7cc2b5c283fb265397912cd63c4b53c83223ebcac9/python-ldap-2.4.25.tar.gz#md5=21523bf21dbe566e0259030f66f7a487
     Processing python-ldap-2.4.25.tar.gz
     Writing /tmp/easy_install-AKouAl/python-ldap-2.4.25/setup.cfg
     Running python-ldap-2.4.25/setup.py -q bdist_egg --dist-dir /tmp/easy_install-AKouAl/python-ldap-2.4.25/egg-dist-tmp-iyQYsJ
     defines: HAVE_SASL HAVE_TLS HAVE_LIBLDAP_R
     extra_compile_args: 
     extra_objects: 
     include_dirs: /usr/include /usr/include/sasl /usr/local/include /usr/local/include/sasl
     library_dirs: /usr/lib /usr/lib64 /usr/local/lib /usr/local/lib64
     libs: ldap_r
     creating /usr/lib/python2.7/site-packages/python_ldap-2.4.25-py2.7-linux-x86_64.egg
     Extracting python_ldap-2.4.25-py2.7-linux-x86_64.egg to /usr/lib/python2.7/site-packages
     Adding python-ldap 2.4.25 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/python_ldap-2.4.25-py2.7-linux-x86_64.egg
     Searching for pyexcel-ods3>=0.1.1
     Reading https://pypi.python.org/simple/pyexcel-ods3/
     Best match: pyexcel-ods3 0.2.0
     Downloading https://pypi.python.org/packages/e0/84/8ce15c7b4ea392fb560cd43a6de0cd8b5f4803832eb26e5b141c34e03da5/pyexcel-ods3-0.2.0.zip#md5=1985c2f3ceb9337b1bcc9503660b8d45
     Processing pyexcel-ods3-0.2.0.zip
     Writing /tmp/easy_install-Vb7oZU/pyexcel-ods3-0.2.0/setup.cfg
     Running pyexcel-ods3-0.2.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-Vb7oZU/pyexcel-ods3-0.2.0/egg-dist-tmp-2oGrgG
     creating /usr/lib/python2.7/site-packages/pyexcel_ods3-0.2.0-py2.7.egg
     Extracting pyexcel_ods3-0.2.0-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding pyexcel-ods3 0.2.0 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/pyexcel_ods3-0.2.0-py2.7.egg
     Searching for pyexcel-xlsx>=0.1.0
     Reading https://pypi.python.org/simple/pyexcel-xlsx/
     Best match: pyexcel-xlsx 0.2.0
     Downloading https://pypi.python.org/packages/0e/79/14739d317451e8ceed934075c49541336d8c3d0ddad53e946bffdb47ac6d/pyexcel-xlsx-0.2.0.zip#md5=9139b9bdcaf2f185abab31337a40cf05
     Processing pyexcel-xlsx-0.2.0.zip
     Writing /tmp/easy_install-ZP3aej/pyexcel-xlsx-0.2.0/setup.cfg
     Running pyexcel-xlsx-0.2.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-ZP3aej/pyexcel-xlsx-0.2.0/egg-dist-tmp-iYs5i4
     creating /usr/lib/python2.7/site-packages/pyexcel_xlsx-0.2.0-py2.7.egg
     Extracting pyexcel_xlsx-0.2.0-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding pyexcel-xlsx 0.2.0 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/pyexcel_xlsx-0.2.0-py2.7.egg
     Searching for pyexcel>=0.2.0
     Reading https://pypi.python.org/simple/pyexcel/
     Best match: pyexcel 0.2.2
     Downloading https://pypi.python.org/packages/ae/bb/b4f31f93be6a283816c89fa6fb2608bca58aac7aeeb4df9d46da956389d8/pyexcel-0.2.2.zip#md5=a939ea1841343d533fb31332dcb66ccf
     Processing pyexcel-0.2.2.zip
     Writing /tmp/easy_install-22C1bY/pyexcel-0.2.2/setup.cfg
     Running pyexcel-0.2.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-22C1bY/pyexcel-0.2.2/egg-dist-tmp-YBUk66
     creating /usr/lib/python2.7/site-packages/pyexcel-0.2.2-py2.7.egg
     Extracting pyexcel-0.2.2-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding pyexcel 0.2.2 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/pyexcel-0.2.2-py2.7.egg
     Searching for paramiko>=1.16.0
     Reading https://pypi.python.org/simple/paramiko/
     Best match: paramiko 2.0.1
     Downloading https://pypi.python.org/packages/b5/dd/cc2b8eb360e3db2e65ad5adf8cb4fd57493184e3ce056fd7625e9c387bfa/paramiko-2.0.1.tar.gz#md5=c00d63b34dcf74649216bdc8875e1ebe
     Processing paramiko-2.0.1.tar.gz
     Writing /tmp/easy_install-dUp2rv/paramiko-2.0.1/setup.cfg
     Running paramiko-2.0.1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-dUp2rv/paramiko-2.0.1/egg-dist-tmp-XhXkXr
     Moving paramiko-2.0.1-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding paramiko 2.0.1 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/paramiko-2.0.1-py2.7.egg
     Searching for MySQL-python>=1.2.3
     Reading https://pypi.python.org/simple/MySQL-python/
     Best match: MySQL-python 1.2.5
     Downloading https://pypi.python.org/packages/a5/e9/51b544da85a36a68debe7a7091f068d802fc515a3a202652828c73453cad/MySQL-python-1.2.5.zip#md5=654f75b302db6ed8dc5a898c625e030c
     Processing MySQL-python-1.2.5.zip
     Writing /tmp/easy_install-_DyIWR/MySQL-python-1.2.5/setup.cfg
     Running MySQL-python-1.2.5/setup.py -q bdist_egg --dist-dir /tmp/easy_install-_DyIWR/MySQL-python-1.2.5/egg-dist-tmp-tA098L
     Moving MySQL_python-1.2.5-py2.7-linux-x86_64.egg to /usr/lib/python2.7/site-packages
     Adding MySQL-python 1.2.5 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/MySQL_python-1.2.5-py2.7-linux-x86_64.egg
     Searching for jsonlib2>=1.5.2
     Reading https://pypi.python.org/simple/jsonlib2/
     Best match: jsonlib2 1.5.2
     Downloading https://pypi.python.org/packages/0e/1d/745b4e69ca0710215f7291ebbdfcdc95896dec7e196312b29d5a7c606038/jsonlib2-1.5.2.tar.gz#md5=f650c6979c04ed128e76edaa9ba50323
     Processing jsonlib2-1.5.2.tar.gz
     Writing /tmp/easy_install-uZftqn/jsonlib2-1.5.2/setup.cfg
     Running jsonlib2-1.5.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-uZftqn/jsonlib2-1.5.2/egg-dist-tmp-xQX9Ii
     Moving jsonlib2-1.5.2-py2.7-linux-x86_64.egg to /usr/lib/python2.7/site-packages
     Adding jsonlib2 1.5.2 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/jsonlib2-1.5.2-py2.7-linux-x86_64.egg
     Searching for httplib2>=0.9.1
     Reading https://pypi.python.org/simple/httplib2/
     Best match: httplib2 0.9.2
     Downloading https://pypi.python.org/packages/ff/a9/5751cdf17a70ea89f6dde23ceb1705bfb638fd8cee00f845308bf8d26397/httplib2-0.9.2.tar.gz#md5=bd1b1445b3b2dfa7276b09b1a07b7f0e
     Processing httplib2-0.9.2.tar.gz
     Writing /tmp/easy_install-EzBORb/httplib2-0.9.2/setup.cfg
     Running httplib2-0.9.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-EzBORb/httplib2-0.9.2/egg-dist-tmp-EFF6cn
     creating /usr/lib/python2.7/site-packages/httplib2-0.9.2-py2.7.egg
     Extracting httplib2-0.9.2-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding httplib2 0.9.2 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/httplib2-0.9.2-py2.7.egg
     Searching for ezodf>=0.3.2
     Reading https://pypi.python.org/simple/ezodf/
     Best match: ezodf 0.3.2
     Downloading https://pypi.python.org/packages/6f/c5/e966935c26d58d7e3d962270be61be972409084374d4093f478d1f82e8af/ezodf-0.3.2.tar.gz#md5=b12670b60b49d3c35338fd46493071fc
     Processing ezodf-0.3.2.tar.gz
     Writing /tmp/easy_install-j1wCSe/ezodf-0.3.2/setup.cfg
     Running ezodf-0.3.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-j1wCSe/ezodf-0.3.2/egg-dist-tmp-Kkst3Q
     Moving ezodf-0.3.2-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding ezodf 0.3.2 to easy-install.pth file
     
     Installed /usr/lib/python2.7/site-packages/ezodf-0.3.2-py2.7.egg
     Searching for pyexcel-io>=0.1.0
     Reading https://pypi.python.org/simple/pyexcel-io/
     Best match: pyexcel-io 0.2.0
     Downloading https://pypi.python.org/packages/43/39/8f2cea9f97ca057da858565347070ee1aa0f748f1232f00d9370c7ab5ff2/pyexcel-io-0.2.0.zip#md5=2f2ea9e662e1ad541dea96f8259fb9f8
     Processing pyexcel-io-0.2.0.zip
     Writing /tmp/easy_install-_AR9yE/pyexcel-io-0.2.0/setup.cfg
     Running pyexcel-io-0.2.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-_AR9yE/pyexcel-io-0.2.0/egg-dist-tmp-s29SXf
     creating /usr/lib/python2.7/site-packages/pyexcel_io-0.2.0-py2.7.egg
     Extracting pyexcel_io-0.2.0-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding pyexcel-io 0.2.0 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/pyexcel_io-0.2.0-py2.7.egg
     Searching for openpyxl>=2.2.2
     Reading https://pypi.python.org/simple/openpyxl/
     Best match: openpyxl 2.4.0b1
     Downloading https://pypi.python.org/packages/25/69/7976ba24d2b532e96157623daa8de4bbcad23e0761b3062d5e38775577d5/openpyxl-2.4.0-b1.tar.gz#md5=f56975d698cbfa619a8c99ddce41b142
     Processing openpyxl-2.4.0-b1.tar.gz
     Writing /tmp/easy_install-as552N/openpyxl-2.4.0-b1/setup.cfg
     Running openpyxl-2.4.0-b1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-as552N/openpyxl-2.4.0-b1/egg-dist-tmp-8V07ey
     creating /usr/lib/python2.7/site-packages/openpyxl-2.4.0b1-py2.7.egg
     Extracting openpyxl-2.4.0b1-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding openpyxl 2.4.0b1 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/openpyxl-2.4.0b1-py2.7.egg
     Searching for texttable>=0.8.1
     Reading https://pypi.python.org/simple/texttable/
     Best match: texttable 0.8.4
     Downloading https://pypi.python.org/packages/f5/5e/47cbc50187ca719a39ce4838182c6126487ca62ddd299bc34cafb94260fe/texttable-0.8.4.tar.gz#md5=6335edbe1bb4edacce7c2f76195f6212
     Processing texttable-0.8.4.tar.gz
     Writing /tmp/easy_install-hGRpsD/texttable-0.8.4/setup.cfg
     Running texttable-0.8.4/setup.py -q bdist_egg --dist-dir /tmp/easy_install-hGRpsD/texttable-0.8.4/egg-dist-tmp-whNOAV
     Moving texttable-0.8.4-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding texttable 0.8.4 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/texttable-0.8.4-py2.7.egg
     Searching for pyasn1>=0.1.7
     Reading https://pypi.python.org/simple/pyasn1/
     Best match: pyasn1 0.1.9
     Downloading https://pypi.python.org/packages/c3/ea/03328a42adfc16a1babbe334ad969f6e27862bcaff9576444d423d2c9257/pyasn1-0.1.9-py2.7.egg#md5=08eef0e822233609f6cad55b419ae00c
     Processing pyasn1-0.1.9-py2.7.egg
     Moving pyasn1-0.1.9-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding pyasn1 0.1.9 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/pyasn1-0.1.9-py2.7.egg
     Searching for cryptography>=1.1
     Reading https://pypi.python.org/simple/cryptography/
     Best match: cryptography 1.4
     Downloading https://pypi.python.org/packages/a9/5b/a383b3a778609fe8177bd51307b5ebeee369b353550675353f46cb99c6f0/cryptography-1.4.tar.gz#md5=a9763e3831cc7cdb402c028fac1ceb39
     Processing cryptography-1.4.tar.gz
     Writing /tmp/easy_install-UWBcIj/cryptography-1.4/setup.cfg
     Running cryptography-1.4/setup.py -q bdist_egg --dist-dir /tmp/easy_install-UWBcIj/cryptography-1.4/egg-dist-tmp-ddL9DI

     Installed /tmp/easy_install-UWBcIj/cryptography-1.4/.eggs/cffi-1.7.0-py2.7-linux-x86_64.egg
     Searching for pycparser
     Reading https://pypi.python.org/simple/pycparser/
     Best match: pycparser 2.14
     Downloading https://pypi.python.org/packages/6d/31/666614af3db0acf377876d48688c5d334b6e493b96d21aa7d332169bee50/pycparser-2.14.tar.gz#md5=a2bc8d28c923b4fe2b2c3b4b51a4f935
     Processing pycparser-2.14.tar.gz
     Writing /tmp/easy_install-UWBcIj/cryptography-1.4/temp/easy_install-gwJjP9/pycparser-2.14/setup.cfg
     Running pycparser-2.14/setup.py -q bdist_egg --dist-dir /tmp/easy_install-UWBcIj/cryptography-1.4/temp/easy_install-gwJjP9/pycparser-2.14/egg-dist-tmp-ouJWBd
     Moving pycparser-2.14-py2.7.egg to /tmp/easy_install-UWBcIj/cryptography-1.4/.eggs

     Installed /tmp/easy_install-UWBcIj/cryptography-1.4/.eggs/pycparser-2.14-py2.7.egg
     creating /usr/lib/python2.7/site-packages/cryptography-1.4-py2.7-linux-x86_64.egg
     Extracting cryptography-1.4-py2.7-linux-x86_64.egg to /usr/lib/python2.7/site-packages
     Adding cryptography 1.4 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/cryptography-1.4-py2.7-linux-x86_64.egg
     Searching for et_xmlfile
     Reading https://pypi.python.org/simple/et_xmlfile/
     Best match: et-xmlfile 1.0.1
     Downloading https://pypi.python.org/packages/22/28/a99c42aea746e18382ad9fb36f64c1c1f04216f41797f2f0fa567da11388/et_xmlfile-1.0.1.tar.gz#md5=f47940fd9d556375420b2e276476cfaf
     Processing et_xmlfile-1.0.1.tar.gz
     Writing /tmp/easy_install-M2dSBT/et_xmlfile-1.0.1/setup.cfg
     Running et_xmlfile-1.0.1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-M2dSBT/et_xmlfile-1.0.1/egg-dist-tmp-XOKuRk
     creating /usr/lib/python2.7/site-packages/et_xmlfile-1.0.1-py2.7.egg
     Extracting et_xmlfile-1.0.1-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding et-xmlfile 1.0.1 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/et_xmlfile-1.0.1-py2.7.egg
     Searching for jdcal
     Reading https://pypi.python.org/simple/jdcal/
     Best match: jdcal 1.2
     Downloading https://pypi.python.org/packages/37/36/3199cfb80fcbf4e4df3a43647733d4f429862c6c97aeadd757613b9e6830/jdcal-1.2.tar.gz#md5=ab8d5ba300fd1eb01514f363d19b1eb9
     Processing jdcal-1.2.tar.gz
     Writing /tmp/easy_install-0U4zpE/jdcal-1.2/setup.cfg
     Running jdcal-1.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-0U4zpE/jdcal-1.2/egg-dist-tmp-Mdfsfa
     Moving jdcal-1.2-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding jdcal 1.2 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/jdcal-1.2-py2.7.egg
     Searching for cffi>=1.4.1
     Reading https://pypi.python.org/simple/cffi/
     Best match: cffi 1.7.0
     Downloading https://pypi.python.org/packages/83/3c/00b553fd05ae32f27b3637f705c413c4ce71290aa9b4c4764df694e906d9/cffi-1.7.0.tar.gz#md5=34122a545060cee58bab88feab57006d
     Processing cffi-1.7.0.tar.gz
     Writing /tmp/easy_install-OkYe7b/cffi-1.7.0/setup.cfg
     Running cffi-1.7.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-OkYe7b/cffi-1.7.0/egg-dist-tmp-557Zw2
     creating /usr/lib/python2.7/site-packages/cffi-1.7.0-py2.7-linux-x86_64.egg
     Extracting cffi-1.7.0-py2.7-linux-x86_64.egg to /usr/lib/python2.7/site-packages
     Adding cffi 1.7.0 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/cffi-1.7.0-py2.7-linux-x86_64.egg
     Searching for ipaddress
     Reading https://pypi.python.org/simple/ipaddress/
     Best match: ipaddress 1.0.16
     Downloading https://pypi.python.org/packages/cd/c5/bd44885274379121507870d4abfe7ba908326cf7bfd50a48d9d6ae091c0d/ipaddress-1.0.16.tar.gz#md5=1e27b62aa20f5b6fc200b2bdbf0d0847
     Processing ipaddress-1.0.16.tar.gz
     Writing /tmp/easy_install-ni9_z4/ipaddress-1.0.16/setup.cfg
     Running ipaddress-1.0.16/setup.py -q bdist_egg --dist-dir /tmp/easy_install-ni9_z4/ipaddress-1.0.16/egg-dist-tmp-ZJzlgP
     Moving ipaddress-1.0.16-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding ipaddress 1.0.16 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/ipaddress-1.0.16-py2.7.egg
     Searching for enum34
     Reading https://pypi.python.org/simple/enum34/
     Best match: enum34 1.1.6
     Downloading https://pypi.python.org/packages/e8/26/a6101edcf724453845c850281b96b89a10dac6bd98edebc82634fccce6a5/enum34-1.1.6.zip#md5=61ad7871532d4ce2d77fac2579237a9e
     Processing enum34-1.1.6.zip
     Writing /tmp/easy_install-8qiMrc/enum34-1.1.6/setup.cfg
     Running enum34-1.1.6/setup.py -q bdist_egg --dist-dir /tmp/easy_install-8qiMrc/enum34-1.1.6/egg-dist-tmp-LhjnCM
     Moving enum34-1.1.6-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding enum34 1.1.6 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/enum34-1.1.6-py2.7.egg
     Searching for six>=1.4.1
     Reading https://pypi.python.org/simple/six/
     Best match: six 1.10.0
     Downloading https://pypi.python.org/packages/b3/b2/238e2590826bfdd113244a40d9d3eb26918bd798fc187e2360a8367068db/six-1.10.0.tar.gz#md5=34eed507548117b2ab523ab14b2f8b55
     Processing six-1.10.0.tar.gz
     Writing /tmp/easy_install-Y7iNXi/six-1.10.0/setup.cfg
     Running six-1.10.0/setup.py -q bdist_egg --dist-dir /tmp/easy_install-Y7iNXi/six-1.10.0/egg-dist-tmp-f68d_B
     creating /usr/lib/python2.7/site-packages/six-1.10.0-py2.7.egg
     Extracting six-1.10.0-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding six 1.10.0 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/six-1.10.0-py2.7.egg
     Searching for idna>=2.0
     Reading https://pypi.python.org/simple/idna/
     Best match: idna 2.1
     Downloading https://pypi.python.org/packages/fb/84/8c27516fbaa8147acd2e431086b473c453c428e24e8fb99a1d89ce381851/idna-2.1.tar.gz#md5=f6473caa9c5e0cc1ad3fd5d04c3c114b
     Processing idna-2.1.tar.gz
     Writing /tmp/easy_install-h9uo0P/idna-2.1/setup.cfg
     Running idna-2.1/setup.py -q bdist_egg --dist-dir /tmp/easy_install-h9uo0P/idna-2.1/egg-dist-tmp-SuVx6u
     Moving idna-2.1-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding idna 2.1 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/idna-2.1-py2.7.egg
     Searching for pycparser
     Reading https://pypi.python.org/simple/pycparser/
     Best match: pycparser 2.14
     Downloading https://pypi.python.org/packages/6d/31/666614af3db0acf377876d48688c5d334b6e493b96d21aa7d332169bee50/pycparser-2.14.tar.gz#md5=a2bc8d28c923b4fe2b2c3b4b51a4f935
     Processing pycparser-2.14.tar.gz
     Writing /tmp/easy_install-s9jZhU/pycparser-2.14/setup.cfg
     Running pycparser-2.14/setup.py -q bdist_egg --dist-dir /tmp/easy_install-s9jZhU/pycparser-2.14/egg-dist-tmp-IWFYrn
     Moving pycparser-2.14-py2.7.egg to /usr/lib/python2.7/site-packages
     Adding pycparser 2.14 to easy-install.pth file

     Installed /usr/lib/python2.7/site-packages/pycparser-2.14-py2.7.egg
     Searching for pycurl==7.19.5.1
     Best match: pycurl 7.19.5.1
     Adding pycurl 7.19.5.1 to easy-install.pth file

     Using /usr/lib64/python2.7/site-packages
     Searching for psycopg2==2.6.1
     Best match: psycopg2 2.6.1
     Adding psycopg2 2.6.1 to easy-install.pth file

     Using /usr/lib64/python2.7/site-packages
     Searching for lxml==3.4.4
     Best match: lxml 3.4.4
     Adding lxml 3.4.4 to easy-install.pth file

     Using /usr/lib64/python2.7/site-packages
     Searching for hydratk==0.3.0a0.dev1
     Best match: hydratk 0.3.0a0.dev1
     Processing hydratk-0.3.0a0.dev1-py2.7.egg
     hydratk 0.3.0a0.dev1 is already the active version in easy-install.pth
     
     **************************************
     *     Running post-install tasks     *
     **************************************                
     
     *** Running task: compile_java_classes ***

     Compiling DBClient.java
     Compiling JMSClient.java     
     
  .. note::
  
     Libraries are installed using yum package manager. 
     Module cx_Oracle installs: libaio
     Module lxml install: python-lxml, libxml2-devel, libxslt-devel
     Module MySQL-python installs: mysql-devel
     Module paramiko installs: libffi-devel, openssl-devel
     Module psycopg2 installs: python-psycopg2
     Module pycurl installs: python-pycurl, libcurl-devel
     Module python-ldap installs: openldap-devel
     Module selenium installs: fontconfig      
     
Run
^^^

When installation is finished you can run the application.

Check hydratk-lib-network module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk
     
     hydratk (0.3.0a0.dev1)
     hydratk-lib-network (0.1.0)
    
Application installs following (paths depend on your OS configuration)

* modules in /usr/local/lib/python2.7/dist-packages/hydratk-lib-network-0.1.0-py2.7egg 
* application folder in /var/local/hydratk/java with files javaee.jar, DBClient.java, DBClient.class, JMSClient.java, JMSClient.class, JMSMessage.class      