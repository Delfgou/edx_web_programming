import smtplib

import config

EMAIL_TO = "c_delfgou1@hotmail.com"

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_FROM,config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject,msg)
        server.sendmail(config.EMAIL_FROM,EMAIL_TO, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")
        
subject = "Welcome to books3000"
msg = "Thank you for your registration."
send_email(subject,msg)