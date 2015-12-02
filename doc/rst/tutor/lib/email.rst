.. Email

=====
Email
=====

Library hydratk.lib.network.email.client provides email client.

**Supported protocols**:

- SMTP
- SMTPS
- IMAP
- IMAPS
- POP
- POPS

**Methods**:

- **connect** - connect to mail server as sender (SMTP, SMTPS) or receiver (IMAP, IMAPS, POP, POPS)
- **disconnect** - disconnect from mail server
- **send_email** - send email (SMTP, SMTPS)
- **email_count** - count emails stored on server (IMAP, IMAPS, POP, POPS)
- **list_emails** - get list of emails stored on server (IMAP, IMAPS, POP, POPS)
- **receive_email** - receive email (IMAP, IMAP, POP, POPS)

Examples
========

See following examples for SMTP, IMAP, POP protocols.
Secured protocol variants are used in similar way.

SMTP
^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.email.client as email
    
     # initialize client
     client = email.EmailClient('smtp')
     
     # connect to SMTP server
     # returns bool
     client.connect(host='smtp.seznam.cz', user='lynushydra', passw='bowman')
     
     # send email
     subject = 'Hydra'
     message = 'This is testing email'
     sender = 'lynushydra@seznam.cz'
     recipients = ['lynushydra@seznam.cz']
     cc = ['lynus@gmail.com']
     bcc = ['lynus@gmail.com']
     
     # returns bool
     client.send_email(subject, message, recipients, cc, bcc) 
     
     # disconnect from server
     # returns bool
     client.disconnect()

IMAP
^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.email.client as email
    
     # initialize client
     client = email.EmailClient('imap')
     
     # connect to IMAP server
     # returns bool
     client.connect(host='imap.seznam.cz', user='lynushydra', passw='bowman')
     
     # count emails
     count = client.email_count()
     
     # get email list
     # returns IDs
     emails = client.list_emails() 
     
     # receive email with ID 2
     sender, recipients, cc, subject, message = client.receive_email(2)

POP
^^^  

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.email.client as email
    
     # initialize client
     client = email.EmailClient('imap')
     
     # connect to IMAP server
     # returns bool
     client.connect(host='pop3.seznam.cz', user='lynushydra', passw='bowman')
     
     # count emails
     count = client.email_count()
     
     # get email list
     # returns IDs
     emails = client.list_emails() 
     
     # receive email with ID 2
     sender, recipients, cc, subject, message = client.receive_email(2)