import smtplib


class EmailClient:
    def __init__(self):
        self.email="fypemail98@gmail.com"
        self.password="wkfxtfkxgdlhjiaq"
    
    def sendEmail(self, receiverEmail, message):
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("fypemail98@gmail.com", "wkfxtfkxgdlhjiaq")
        # sending the mail
        s.sendmail("fypemail98@gmail.com", receiverEmail, message)
        # terminating the session
        s.quit()

#test code--------------------------------------------------
email_Client=EmailClient()
email_Client.sendEmail("tharindathamaranga98@gmail.com","hi Im tharinda")