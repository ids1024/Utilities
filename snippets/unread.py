#!/usr/bin/python

#Checks if any unread emails in a maildir are in abook contacts

#Notes:
# - Original used mailbox.Maildir--Far slower
# - HeaderParser caused encoding issues

import os
import abook
from email.utils import parseaddr
from email.parser import BytesHeaderParser

inbox = "/home/ian/.mail/INBOX"
addressbook = abook.get_abook()
unread = False
parser = BytesHeaderParser()

os.chdir(inbox+"/new")
for i in os.listdir():
    with open(i, 'rb') as file:
        email = parser.parse(file)
    if parseaddr(email.get('from'))[1] in addressbook:
        unread = True
        break
print(unread)
