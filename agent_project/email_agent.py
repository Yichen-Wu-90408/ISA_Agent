import smtplib, os
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pdf_agent import pdf_generation
from excel_agent import write_summary, write_details

def send_email(smtpHost,port, sendAddr, password, recipientAddrs, subject='', content=''):
    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = sendAddr
    msg['to'] = recipientAddrs
    msg['subject'] = subject
    content = content
    txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
    msg.attach(txt)
    print("prepare to add attachment ...")
    part = MIMEApplication(open('Daily_Report.pdf','rb').read())
    part.add_header('Content-Disposition', 'attachment', filename="Daily Report.pdf")
    msg.attach(part)
    part = MIMEApplication(open('../PROJECT SUMMARY.xls','rb').read())
    part.add_header('Content-Disposition', 'attachment', filename="PROJECT SUMMARY.xls")
    msg.attach(part)
    part = MIMEApplication(open('../PROJECT DETAILS.xls','rb').read())
    part.add_header('Content-Disposition', 'attachment', filename="PROJECT DETAILS.xls")
    msg.attach(part)
    smtp = smtplib.SMTP_SSL(smtpHost, port)
    smtp.login(sendAddr, password)
    smtp.sendmail(sendAddr, recipientAddrs.split(";"), str(msg))
    print("sent successfully!")
    smtp.quit()

def run_email_agent():
    summary = write_summary()
    details = write_details()
    generation = pdf_generation()
    try:       
        smtpHost = 'smtp.163.com'
        port = 465 
        sendAddr ='csyxni2020@163.com'
        password = 'XHZTDPLZCIZFUPKR'
        recipientAddrs = 'e0703591@u.nus.edu;e0703361@u.nus.edu;zengzijing1@163.com;e0703576@u.nus.edu'
        subject='Daily Report (PDF)'
        content='Here is today\'s report, please see the attachment.'
        send_email(smtpHost, port, sendAddr, password, recipientAddrs, subject, content)
    except Exception as err:
        print(err)

run_email_agent()