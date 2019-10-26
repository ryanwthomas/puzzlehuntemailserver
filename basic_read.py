import email, email.utils
import imaplib
import itertools

debug = True

# one time
username = 'umdpuzzlehunt@gmail.com'
password = input("Enter password: ")

# open connect
# log into email
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)

if debug:
    print( mail.select("inbox") )

mail.select("inbox")

# get data about emails
result, data = mail.uid('search', None, "ALL")

# get list of email IDs
inbox_item_list = data[0].split()

if debug:
    print(inbox_item_list)

index = -1

# get indexth email
item = inbox_item_list[index]

if debug:
    print(item)

# for item in inbox_item_list:

result2, email_data = mail.uid('fetch', item, '(RFC822)')

raw_email = email_data[0][1].decode("utf-8")

# print( raw_email )

email_message = email.message_from_string(raw_email)

dir(email_message)
if debug:
    print( dir(email_message) )

recipient = email_message['To']
sender = email_message['From']
subject = email_message['Subject']
date = email_message['date']

time_tuple = email.utils.parsedate( date )
print( time_tuple )

# print (time_tuple.__class__.__name__)

if debug:
    print( recipient )
    print( sender )
    print( subject )
    print( date )
    # print( email_message.get_payload() )

counter = 1
for part in email_message.walk():
    if part.get_content_maintype() == "multipart":
        continue
    # filename = part.get_filename()
    # if not filename:
    #     ext = '.html'
    #     filename = 'msg-part-%08d%s' %(counter, ext)
    counter += 1

    content_type = part.get_content_type()

    if debug:
        print(content_type )
        if "plain" in content_type:
            print('>%s<'%part.get_payload())
        else:
            print("not plain text")

if debug:
    print(subject)

# desti_folder_name = "Processed"
# src_folder_name = 'ALL'
#
# typ, data = mail.uid('STORE', inbox_item_list[index], '+X-GM-LABELS', desti_folder_name )
# typ, data = mail.uid('STORE', inbox_item_list[index], '-X-GM-LABELS', src_folder_name )

# mail.uid('STORE', inbox_item_list[index], '+FLAGS', "\\Deleted")
# mail.expunge()
mail.close()
mail.logout()
