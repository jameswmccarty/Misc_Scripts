import smtplib
import os
import getpass
import sys
import ssl
import time
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

def MailingMain():
	fromaddr = 'noreply@example.com'
	password = input("Enter Your Password: ")
	toaddr =  "user@example.com"
	subject = "E-mail Message"
	pathfile = "e-mail_body_as_html_file.html"

	html = open(pathfile)
	msg = MIMEText(html.read(), 'html')
	msg['To'] = toaddr
	msg['Subject'] = subject

	server = smtplib.SMTP('mail.example.com', 587)
	server.starttls()
	server.login(fromaddr, password)
	text = msg.as_string()
	print(server.sendmail(fromaddr, toaddr, text))
	server.quit()
	print("Email Sent")


if __name__=="__main__":
	MailingMain()
