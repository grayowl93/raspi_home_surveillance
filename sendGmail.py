import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

def sendMsg_eMail(from_address, to_address, cc_address, subject, body, encode):
#	gmail_addr=from_address
	gmail_pass=""
	SMTP="smtp.gmail.com"
	PORT=587
#	from_addr= gmail_addr
#	to_addr="grayowl93@yahoo.co.jp"
#	subject="zushi pi"
#	body="test send"
	msg=MIMEText(body,"plain",encode)
	msg["From"]=from_address
	msg["To"]=to_address
	msg["Subject"]=Header(subject, encode)

	try:
		print("mail Sending now...")
		send = smtplib.SMTP(SMTP,PORT)
#		send.set_debuglevel(True)
		send.ehlo()
		send.starttls()
		send.ehlo()
		send.login(from_address,gmail_pass)
		send.send_message(msg)
		send.close()
	except Exception as e:
		print("except: "+str(e))
	else:
		print("{0} send message.".format(to_address))

if __name__ == "__main__":
	mail_to="grayowl93@yahoo.co.jp"
	mail_from="yardbirds.zushi7541@gmail.com"
	mail_cc="grayowl93@i.softbank.jp"
	mail_subject="test pi"
	mail_body="test"
	mail_encode="utf-8"
	sendMsg_eMail(mail_from, mail_to, mail_cc, mail_subject, mail_body, mail_encode)

