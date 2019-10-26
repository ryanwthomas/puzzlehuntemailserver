import smtplib, ssl
import time

class EmailSender:
    def __init__(self, sender, password, send_emails=True):
        self.password = password
        self.sender = sender
        self.send_emails = send_emails

    def send_basic_email(self, message, recipient):
        if self.send_emails:
            time.sleep(5)
            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"

            if message[0:8] != "Subject:":
                message = "Subject: "+message

            message.encode(encoding='UTF-8', errors='strict')

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, recipient, str(message))
                # server.logout()

    def send_email_ff(self, filename, recipient, data):
        tempfile = open(filename, 'r')
        f = tempfile.readlines()
        tempfile.close()

        message = ""
        for x in f:
            message += str(x)+"\r\n"

        message = message % data

        self.send_basic_email(message, recipient)

#
#
# e = EmailSender('umdpuzzlehunt@gmail.com', 'wildgoosechase')
# e.send_email_from_file('subject_dne.txt', 'ryan.w.thomas@live.com',())
# print("hello")
