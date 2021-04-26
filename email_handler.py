from logger import log, debug
from getpass import getpass
import imaplib
import json
import email
import os

class emailHandler:

    def __init__(self):
        with open("config.json") as config_file:
            self.config = json.load(config_file)
        self.host = "imap.gmail.com"
        print("please enter the password for your email account")
        self.pwd = getpass()
        self.usr = self.config["Email"]
        self.media_list = []
        log("got email credentials")
        
    def connect(self):
        log("try to connect")
        self.mail = imaplib.IMAP4_SSL(self.host)
        self.mail.login(self.usr,self.pwd)
        self.mail.select("inbox")
        log("connected to inbox")

    def getInbox(self):
        typ, self.data = self.mail.search(None, "ALL")
        #f'(SUBJECT {self.config["emailFrom"]})'
        mail_ids = self.data[0]
        mail_ids = self.data[0]
        self.id_list = mail_ids.split()
        #debug("getInbox",self.id_list)
        log("got Inbox content")

    def getPath(self,ticket_id=0):
        #Sets the path where the email attachments are to be saved.
        abs_path = os.getcwd()
        media_folder = os.path.join(abs_path,'media')
        if not os.path.isdir(media_folder):
            os.mkdir(media_folder)
        file_name = f"ticket no{ticket_id}.pdf"
        media_path = os.path.join(media_folder, file_name)
        return media_path


    def downloadAttchments(self):
        log("start to download attchments")
        for num,id in enumerate(self.data[0].split()):
            #debug("downloadAttchments",id)
            typ, data = self.mail.fetch(id, '(RFC822)')
            raw_email = data[0][1]
            raw_email_string = raw_email.decode("utf-8")
            email_msg = email.message_from_string(raw_email_string)

            for part in email_msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if bool(filename):
                    file_path = self.getPath(ticket_id=num)
                    media = open(file_path, "wb")
                    media.write(part.get_payload(decode=True))
                    media.close()
                    self.media_list.append(file_path)
            log(f"attchments downloaded {num+1}/{len(self.data[0].split())}")

    def startEmailHandler(self):
        self.connect()
        self.getInbox()
        self.downloadAttchments()
        self.mail.logout
        return self.media_list

            



#emailClient = emailHandler()
#emailClient.startEmailHandler()