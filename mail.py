from imports import *

def send_mail(zipfile_name, receiver_address):
    mail_content_file = open('mail_body.txt')
    sender_address = 'deshpandesaarth@gmail.com'
    sender_pass = 'xxxxxx'
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Chapter Summaries Attached'
    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content_file.read(), 'plain'))
    attach_file_name = f'{zipfile_name}'
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('application', 'pdf')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
