import os
from configparser import RawConfigParser

infile = os.path.expanduser("~/.abook/addressbook")

class AddressBook(object):
    def __init__(self, contacts):
        self.contacts = contacts
        for i in self.contacts:
            i["email"] = list(filter(None, i.get("email", '').split(",")))

    def __getitem__(self, key):
        if isinstance(key, str):
            names = [i['name'] for i in self.contacts]
            if key in names:
                return self.contacts[names.index(key)]
            for x, name in enumerate(names):
                if key.lower() in name.lower():
                    return self.contacts[x]
        elif isinstance(key, int):
            return self.contacts[key]
        raise KeyError

    def __len__(self):
        return len(self.contacts)

    def __str__(self):
        return str(self.contacts)
    
    def __unicode__(self):
        return str(self.contacts)

    def __repr__(self):
        return str(self.contacts)

    def __contains__(self, item):
        for i in self.contacts:
            if i['name'] == item or item in i['email']:
                return True
        return False

def get_abook():
    parser = RawConfigParser()
    parser.read(infile)
    contacts = [dict(parser[i]) for i in parser if i.isdigit()]
    return AddressBook(contacts)
