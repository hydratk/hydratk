.. FTP

===
FTP
===

Library hydratk.lib.network.ftp.client provides ftp client.

**Supported protocols**:

- FTP
- FTPS
- SFTP
- TFTP

**Methods**:

- **connect** - connect to server
- **disconnect** - disconnect from server (FTP, FTPS, SFTP)
- **list_dir** - get directory content (FTP, FTPS, SFTP)
- **change_dir** - change remote directory (FTP, FTP, SFTP)
- **download_file** - download file from server
- **upload_file** - upload file to server
- **delete_file** - delete file on server (FTP, FTPS, SFTP)
- **make_dir** - make directory on server (FTP, FTPS, SFTP)
- **remove_dir** - remove directory from server (FTP, FTPS, SFTP)

Examples
========

See following examples for FTP, SFTP, TFTP protocols.
The usage for FTPS protocol is similar to FTP.

FTP
^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.ftp.client import FTPClient as ftp
    
     # initialize client
     client = ftp('ftp')
     
     # connect to FTP server
     # returns bool
     client.connect(host='srv8.endora.cz', user='aaa', passw='bbb')
     
     # change directory
     # returns bool
     client.change_dir('/lynus.cekuj.net/web')
     
     # get directory content
     # returns file and directory names
     names =  client.list_dir()
     
     # download file from server
     # returns bool
     client.download_file('/lynus.cekuj.net/web/index.php') 
     
     # upload file to server
     # returns bool
     client.upload_file('index2.php', '/lynus.cekuj.net/web')
     
     # delete file from server
     # returns bool
     client.delete_file('index2.php')
     
     # make directory on server
     # returns bool
     client.make_dir('pokus2')
     
     # remove directory from server
     # returns bool
     client.remove_dir('pokus2')   
     
     # disconnect from server
     # returns bool
     client.disconnect()

SFTP
^^^^ 

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.ftp.client import FTPClient as ftp
    
     # initialize client 
     client = ftp.FTPClient('sftp')
  
     # connect to SFTP server
     client.connect(host='lxocrmgf401vm.cz', user='aaa', passw='bbb')
     
     # change dicrector
     # returns bool
     client.change_dir('/appl/home/x0549396/portal')
     
     # get directory content
     # returns files and directory names
     client.list_dir()

     # download file from server
     # returns bool
     client.download_file('response.xml')

     # upload file to server
     # returns bool
     client.upload_file('index.php', '/appl/home/portal')
     
     # delete file from server
     # returns bool
     client.delete_file('index.php')
     
     # make directory on server
     # returns bool
     client.make_dir('pokus2')
     
     # remove directory from server
     # returns bool
     client.remove_dir('pokus2')   
     
     # disconnect from server
     # returns bool
     client.disconnect()     

TFTP
^^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.ftp.client import FTPClient as ftp
    
     # initialize client 
     client = ftp.FTPClient('tftp')
     
     # connect to TFTP server
     # returns bool
     client.connect(host='0.0.0.0')  
     
     # download file from server
     # returns bool
     client.download_file('/doc/bdd.txt2')  
     
     # upload file to server
     # returns bool
     client.upload_file('pok.txt', '/doc2') 