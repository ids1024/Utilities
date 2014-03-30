#!/usr/bin/python

#Notes:
# - HeaderParser caused encoding issues

import os
import abook
from email.utils import parseaddr
from email.parser import BytesHeaderParser

#inbox = mailbox.Maildir("/home/ian/.mail/INBOX")
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

#Code from old version, better perhaps, but way slower
#for i in inbox.itervalues():
#    if 'S' in i.get_flags():
#        continue
#    if parseaddr(i.get('from'))[1] in addressbook:
#        unread = True
#        break
#print(unread)


#(i.get('from').split('<')[1][:-1] for i in m.itervalues() if 'S' not in i.get_flags()):
