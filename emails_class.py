import re

class Emails:

    email_list = []
    email_blacklist = ['umdpuzzlehunt@gmail.com']

    def __init__(self, filename):
        self.filename = filename
        tempfile = open(filename, 'r')
        f = tempfile.readlines()
        tempfile.close()

        for line in f:
            self.email_list.append( line.strip().lower() )

    def addEmail(self, new_email):
        new_email = new_email.strip('\n').lower()
        temp = re.search( "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",\
        new_email, re.IGNORECASE)
        new_email = temp.group(1)

        if( not new_email in self.email_list and \
        new_email not in self.email_blacklist ):
            self.email_list.append(new_email)

            # add on to team textfile
            tempfile = open(self.filename, "a+")
            tempfile.write("\r\n%s" % new_email)
            tempfile.close()

# emails = Emails("savefile_emails.txt")
#
# print( emails.email_list)
