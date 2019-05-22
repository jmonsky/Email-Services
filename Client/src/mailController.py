import imaplib
import smtplib
import email
from email.message import EmailMessage
from Email import Email


class MailController(object):
    def __init__(self):
        self.imap = None
        self.smtp = None
        self.address = None
    
    def login(self, username, password, smtp_address, imap_address, smtp_port, imap_port):
        self.imap = imaplib.IMAP4_SSL(imap_address, imap_port)
        self.smtp = smtplib.SMTP_SSL(smtp_address, smtp_port)
        self.imap.login(username, password)
        self.smtp.login(username, password)
        self.address = username

    def disconnect(self):
        self.imap.close()
        self.imap.logout()

    def delMail(self, mail):
        self.imap.store(mail.id, '+FLAGS', '\\Deleted')
        self.imap.expunge()

    def delMails(self, mails):
        for m in mails:
            self.imap.store(m.id, '+FLAGS', '\\Deleted')
        self.imap.expunge()

    def clearInbox(self):
        self.delMails(self.getMail())

    def getMail(self):
        self.imap.select("Inbox")
        _, data = self.imap.search(None, 'ALL')
        id_list = data[0].split()
        mails = []
        for i in id_list:
            _, data = self.imap.fetch(i, '(RFC822)' )
            for x in data:
                if type(x) == tuple:
                    msg = email.message_from_bytes(x[1])
                    mails.append(Email(i, msg))
                    break

        return mails
        

    def sendMail(self, to, subject, body):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["To"] = to
        msg.set_content(body)
        self.smtp.send_message(msg, from_addr=self.address)
